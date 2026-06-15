import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from campaigns.models import Campaign
from contacts.models import ContactListMembership
from email_engine.models import EmailJob
from email_engine.tasks import process_email_job

logger = logging.getLogger(__name__)


def get_campaign_html(campaign):
    """
    Resolve final HTML body for campaign.
    Priority:
    1. campaign.custom_html_content
    2. campaign.template.html_content
    3. fallback text body
    """
    if getattr(campaign, "custom_html_content", ""):
        return campaign.custom_html_content

    template = getattr(campaign, "template", None)
    if template and getattr(template, "html_content", ""):
        return template.html_content

    return f"<p>{campaign.subject}</p>"


def get_campaign_text(campaign):
    """
    Resolve text body for campaign.
    """
    if getattr(campaign, "custom_text_content", ""):
        return campaign.custom_text_content

    template = getattr(campaign, "template", None)
    if template and getattr(template, "text_content", ""):
        return template.text_content

    return campaign.subject or ""


def get_campaign_recipients(campaign):
    """
    Current campaign model sends through:
    Campaign -> target_lists -> ContactListMembership -> Contact
    """
    target_lists = campaign.target_lists.all()

    if not target_lists.exists():
        return []

    contacts = (
        ContactListMembership.objects
        .filter(contact_list__in=target_lists)
        .select_related("contact")
        .values_list("contact", flat=True)
        .distinct()
    )

    from contacts.models import Contact

    return list(
        Contact.objects
        .filter(id__in=contacts, organization=campaign.organization)
        .distinct()
    )


@shared_task
def process_pending_campaigns():
    """
    Find scheduled campaigns that are due and create EmailJob rows.
    Celery beat should call this every few minutes.
    """
    now = timezone.now()

    campaigns = (
        Campaign.objects
        .select_related("organization", "template")
        .prefetch_related("target_lists")
        .filter(
            status="scheduled",
            scheduled_at__lte=now,
        )
    )

    processed = 0
    created_jobs = 0
    failed = 0

    for campaign in campaigns:
        result = process_campaign(campaign.id)
        processed += 1

        if result.get("status") == "queued":
            created_jobs += result.get("created_jobs", 0)
        elif result.get("status") == "failed":
            failed += 1

    logger.info(
        "Processed %s pending campaigns. Created jobs: %s. Failed: %s.",
        processed,
        created_jobs,
        failed,
    )

    return {
        "processed": processed,
        "created_jobs": created_jobs,
        "failed": failed,
    }


@shared_task
def process_campaign(campaign_id):
    """
    Process one campaign:
    - Lock campaign
    - Collect recipients
    - Create EmailJob rows
    - Dispatch EmailJob tasks
    - Mark campaign queued/done based on job creation
    """
    try:
        with transaction.atomic():
            campaign = (
                Campaign.objects
                .select_for_update()
                .select_related("organization", "template")
                .prefetch_related("target_lists")
                .get(id=campaign_id)
            )

            if campaign.status not in ["scheduled", "running"]:
                return {
                    "status": "skipped",
                    "reason": f"Campaign status is {campaign.status}",
                    "campaign_id": str(campaign.id),
                }

            campaign.status = "running"
            campaign.save(update_fields=["status", "updated_at"])

            recipients = get_campaign_recipients(campaign)

            if not recipients:
                campaign.status = "failed"
                campaign.save(update_fields=["status", "updated_at"])

                logger.warning(
                    "Campaign %s failed: no recipients found.",
                    campaign.id,
                )

                return {
                    "status": "failed",
                    "reason": "No recipients found. Add contact lists to this campaign.",
                    "campaign_id": str(campaign.id),
                }

            html_body = get_campaign_html(campaign)
            text_body = get_campaign_text(campaign)

            created_job_ids = []

            for contact in recipients:
                existing = EmailJob.objects.filter(
                    campaign=campaign,
                    contact=contact,
                    recipient_email=contact.email,
                ).first()

                if existing:
                    created_job_ids.append(existing.id)
                    continue

                recipient_name = " ".join(
                    [
                        getattr(contact, "first_name", "") or "",
                        getattr(contact, "last_name", "") or "",
                    ]
                ).strip()

                job = EmailJob.objects.create(
                    campaign=campaign,
                    contact=contact,
                    organization=campaign.organization,
                    email_type="campaign",
                    priority=5,
                    recipient_email=contact.email,
                    recipient_name=recipient_name,
                    recipient_phone=getattr(contact, "phone", "") or "",
                    from_email=getattr(campaign, "from_email", "") or "",
                    from_name=getattr(campaign, "from_name", "") or "",
                    reply_to=getattr(campaign, "reply_to", "") or "",
                    subject_snapshot=campaign.subject,
                    body_snapshot=text_body or html_body,
                    html_body=html_body,
                    status="queued",
                    scheduled_at=timezone.now(),
                    max_attempts=3,
                )

                created_job_ids.append(job.id)

            campaign.total_sent = len(created_job_ids)
            campaign.status = "completed" if created_job_ids else "failed"
            campaign.save(update_fields=["total_sent", "status", "updated_at"])

        for job_id in created_job_ids:
            process_email_job.delay(job_id)

        logger.info(
            "Campaign %s created/dispatched %s email jobs.",
            campaign_id,
            len(created_job_ids),
        )

        return {
            "status": "queued",
            "campaign_id": str(campaign_id),
            "created_jobs": len(created_job_ids),
        }

    except Campaign.DoesNotExist:
        logger.error("Campaign %s not found.", campaign_id)
        return {
            "status": "failed",
            "reason": "Campaign not found.",
            "campaign_id": str(campaign_id),
        }

    except Exception as exc:
        logger.exception("Campaign %s failed: %s", campaign_id, exc)

        try:
            Campaign.objects.filter(id=campaign_id).update(status="failed")
        except Exception:
            pass

        return {
            "status": "failed",
            "reason": str(exc),
            "campaign_id": str(campaign_id),
        }
