from datetime import timedelta

from django.db.models import Count, Max, Sum
from django.utils import timezone

from .models import (
    OrganizationAnalytics,
    CampaignAnalytics,
    DailyAnalytics,
    LinkAnalytics,
)


def safe_rate(numerator, denominator):
    if not denominator:
        return 0.0
    return round((numerator / denominator) * 100, 2)


class AnalyticsService:
    @staticmethod
    def get_active_organization(user):
        return getattr(user, "active_organization", None)

    @classmethod
    def refresh_organization_analytics(cls, organization):
        from campaigns.models import Campaign
        from contacts.models import Contact
        from email_engine.models import EmailJob
        from links.models import TrackedLink, LinkClick
        from webhooks.models import WebhookDelivery

        email_jobs = EmailJob.objects.filter(organization=organization)
        links = TrackedLink.objects.filter(organization=organization)
        clicks = LinkClick.objects.filter(organization=organization)
        deliveries = WebhookDelivery.objects.filter(webhook__organization=organization)

        obj, _ = OrganizationAnalytics.objects.get_or_create(organization=organization)

        obj.total_campaigns = Campaign.objects.filter(organization=organization).count()
        obj.total_contacts = Contact.objects.filter(organization=organization).count()

        obj.total_email_jobs = email_jobs.count()
        obj.total_emails_sent = email_jobs.filter(status="done").count()
        obj.total_emails_failed = email_jobs.filter(status="failed").count()
        obj.total_emails_queued = email_jobs.filter(status="queued").count()

        obj.total_generated_links = links.count()
        obj.total_clicks = clicks.count()
        obj.total_unique_clicks = clicks.filter(is_unique=True).count()
        obj.total_clicked_contacts = clicks.exclude(contact__isnull=True).values("contact").distinct().count()

        obj.total_webhook_deliveries = deliveries.count()
        obj.total_webhook_success = deliveries.filter(success=True).count()
        obj.total_webhook_failures = deliveries.filter(success=False).count()

        obj.last_email_sent_at = email_jobs.filter(status="done").aggregate(Max("sent_at"))["sent_at__max"]
        obj.last_clicked_at = clicks.aggregate(Max("clicked_at"))["clicked_at__max"]
        obj.last_updated_at = timezone.now()
        obj.save()

        return obj

    @classmethod
    def refresh_campaign_analytics(cls, campaign):
        from email_engine.models import EmailJob
        from links.models import TrackedLink, LinkClick

        jobs = EmailJob.objects.filter(campaign=campaign)
        links = TrackedLink.objects.filter(campaign=campaign)
        clicks = LinkClick.objects.filter(campaign=campaign)

        obj, _ = CampaignAnalytics.objects.get_or_create(campaign=campaign)

        obj.total_jobs = jobs.count()
        obj.total_queued = jobs.filter(status="queued").count()
        obj.total_processing = jobs.filter(status="processing").count()
        obj.total_sent = jobs.filter(status="done").count()
        obj.total_failed = jobs.filter(status="failed").count()

        obj.total_delivered = obj.total_sent
        obj.total_opens = 0
        obj.total_clicks = clicks.count()
        obj.unique_clicks = clicks.filter(is_unique=True).count()
        obj.clicked_contacts = clicks.exclude(contact__isnull=True).values("contact").distinct().count()

        obj.total_bounces = 0
        obj.total_unsubscribes = 0
        obj.total_complaints = 0

        obj.recipient_count = jobs.values("recipient_email").distinct().count()
        obj.generated_links = links.count()

        obj.open_rate = safe_rate(obj.total_opens, obj.total_delivered)
        obj.click_rate = safe_rate(obj.total_clicks, obj.total_delivered)
        obj.unique_click_rate = safe_rate(obj.unique_clicks, obj.total_delivered)
        obj.bounce_rate = safe_rate(obj.total_bounces, obj.total_jobs)

        top_link = (
            links.values("original_url")
            .annotate(total=Sum("click_count"))
            .order_by("-total")
            .first()
        )

        obj.top_clicked_url = top_link["original_url"] if top_link else ""
        obj.last_sent_at = jobs.filter(status="done").aggregate(Max("sent_at"))["sent_at__max"]
        obj.last_clicked_at = clicks.aggregate(Max("clicked_at"))["clicked_at__max"]
        obj.last_updated_at = timezone.now()
        obj.save()

        return obj

    @classmethod
    def refresh_all_campaign_analytics(cls, organization=None):
        from campaigns.models import Campaign

        campaigns = Campaign.objects.all()

        if organization:
            campaigns = campaigns.filter(organization=organization)

        count = 0

        for campaign in campaigns:
            cls.refresh_campaign_analytics(campaign)
            count += 1

        return count

    @classmethod
    def refresh_daily_analytics(cls, organization, target_date=None):
        from campaigns.models import Campaign
        from contacts.models import Contact
        from email_engine.models import EmailJob
        from links.models import TrackedLink, LinkClick
        from webhooks.models import WebhookDelivery

        date = target_date or timezone.localdate()

        day_start = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.min.time())
        )
        day_end = day_start + timedelta(days=1)

        jobs = EmailJob.objects.filter(
            organization=organization,
            scheduled_at__gte=day_start,
            scheduled_at__lt=day_end,
        )
        clicks = LinkClick.objects.filter(
            organization=organization,
            clicked_at__gte=day_start,
            clicked_at__lt=day_end,
        )
        links = TrackedLink.objects.filter(
            organization=organization,
            last_clicked_at__gte=day_start,
            last_clicked_at__lt=day_end,
        )
        deliveries = WebhookDelivery.objects.filter(
            webhook__organization=organization,
            created_at__gte=day_start,
            created_at__lt=day_end,
        )

        obj, _ = DailyAnalytics.objects.get_or_create(
            organization=organization,
            date=date,
        )

        obj.active_campaigns = Campaign.objects.filter(
            organization=organization,
            created_at__lt=day_end,
        ).count()
        obj.new_contacts = Contact.objects.filter(
            organization=organization,
            created_at__gte=day_start,
            created_at__lt=day_end,
        ).count()

        obj.email_jobs = jobs.count()
        obj.emails_sent = jobs.filter(status="done").count()
        obj.emails_failed = jobs.filter(status="failed").count()
        obj.emails_queued = jobs.filter(status="queued").count()
        obj.emails_delivered = obj.emails_sent

        obj.opens = 0
        obj.clicks = clicks.count()
        obj.unique_clicks = clicks.filter(is_unique=True).count()
        obj.clicked_contacts = clicks.exclude(contact__isnull=True).values("contact").distinct().count()

        obj.bounces = 0
        obj.unsubscribes = 0

        obj.generated_links = links.count()
        obj.webhook_deliveries = deliveries.count()
        obj.webhook_failures = deliveries.filter(success=False).count()
        obj.save()

        return obj

    @classmethod
    def refresh_link_analytics(cls, organization=None):
        from links.models import TrackedLink, LinkClick

        qs = TrackedLink.objects.all()

        if organization:
            qs = qs.filter(organization=organization)

        groups = (
            qs.values("organization", "campaign", "original_url")
            .annotate(
                generated_links=Count("id"),
                total_clicks=Sum("click_count"),
                unique_clicks=Sum("unique_click_count"),
                last_clicked_at=Max("last_clicked_at"),
            )
        )

        count = 0

        for row in groups:
            clicks = LinkClick.objects.filter(
                organization_id=row["organization"],
                campaign_id=row["campaign"],
                tracked_link__original_url=row["original_url"],
            )

            clicked_contacts = clicks.exclude(contact__isnull=True).values("contact").distinct().count()

            obj, _ = LinkAnalytics.objects.get_or_create(
                organization_id=row["organization"],
                campaign_id=row["campaign"],
                original_url=row["original_url"],
            )

            obj.generated_links = row["generated_links"] or 0
            obj.total_clicks = row["total_clicks"] or 0
            obj.unique_clicks = row["unique_clicks"] or 0
            obj.clicked_contacts = clicked_contacts
            obj.last_clicked_at = row["last_clicked_at"]
            obj.last_updated_at = timezone.now()
            obj.save()

            count += 1

        return count

    @classmethod
    def build_live_overview(cls, organization):
        org_analytics = cls.refresh_organization_analytics(organization)

        return {
            "organization": {
                "id": str(organization.id),
                "name": organization.name,
                "brand_name": getattr(organization, "display_name", organization.name),
            },
            "totals": {
                "campaigns": org_analytics.total_campaigns,
                "contacts": org_analytics.total_contacts,
                "email_jobs": org_analytics.total_email_jobs,
                "sent": org_analytics.total_emails_sent,
                "failed": org_analytics.total_emails_failed,
                "queued": org_analytics.total_emails_queued,
                "generated_links": org_analytics.total_generated_links,
                "clicks": org_analytics.total_clicks,
                "unique_clicks": org_analytics.total_unique_clicks,
                "clicked_contacts": org_analytics.total_clicked_contacts,
                "webhook_deliveries": org_analytics.total_webhook_deliveries,
                "webhook_failures": org_analytics.total_webhook_failures,
            },
            "rates": {
                "click_rate": safe_rate(org_analytics.total_clicks, org_analytics.total_emails_sent),
                "unique_click_rate": safe_rate(org_analytics.total_unique_clicks, org_analytics.total_emails_sent),
                "failure_rate": safe_rate(org_analytics.total_emails_failed, org_analytics.total_email_jobs),
                "webhook_failure_rate": safe_rate(
                    org_analytics.total_webhook_failures,
                    org_analytics.total_webhook_deliveries,
                ),
            },
            "last_activity": {
                "last_email_sent_at": org_analytics.last_email_sent_at,
                "last_clicked_at": org_analytics.last_clicked_at,
                "last_updated_at": org_analytics.last_updated_at,
            },
        }
