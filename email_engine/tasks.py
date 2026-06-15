import logging
from datetime import timedelta

from celery import shared_task
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import EmailJob, SMTPConfig
from .services import EmailJobProcessor, EmailService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def process_email_job(self, job_id):
    try:
        job = (
            EmailJob.objects
            .select_related("organization", "campaign", "contact", "custom_smtp_config")
            .get(id=job_id)
        )
    except EmailJob.DoesNotExist:
        logger.error("EmailJob %s not found", job_id)
        return {"status": "missing", "job_id": str(job_id)}

    if job.status not in ["queued", "processing"]:
        return {"status": "skipped", "job_id": str(job.id), "job_status": job.status}

    if job.next_retry_at and job.next_retry_at > timezone.now():
        return {"status": "retry_later", "job_id": str(job.id)}

    with transaction.atomic():
        locked = EmailJob.objects.select_for_update().get(id=job.id)

        if locked.status not in ["queued", "processing"]:
            return {"status": "skipped", "job_id": str(locked.id), "job_status": locked.status}

        locked.status = "processing"
        locked.save(update_fields=["status"])
        job = locked

    try:
        success, message, smtp_config = EmailJobProcessor.process(job)

        return {
            "status": "sent",
            "job_id": str(job.id),
            "smtp_id": str(smtp_config.id) if smtp_config else None,
            "message": message,
        }

    except Exception as exc:
        error_message = str(exc)

        job.attempts += 1
        job.error_message = error_message

        delay = min(60 * (3 ** max(job.attempts - 1, 0)), 7200)

        if job.attempts >= job.max_attempts:
            job.status = "failed"
            job.next_retry_at = None
            job.save(update_fields=[
                "attempts",
                "error_message",
                "status",
                "next_retry_at",
            ])

            logger.error(
                "EmailJob %s failed after %s attempts: %s",
                job.id,
                job.attempts,
                error_message,
            )

            return {
                "status": "failed",
                "job_id": str(job.id),
                "error": error_message,
            }

        job.status = "queued"
        job.next_retry_at = timezone.now() + timedelta(seconds=delay)
        job.save(update_fields=[
            "attempts",
            "error_message",
            "status",
            "next_retry_at",
        ])

        logger.warning(
            "EmailJob %s failed attempt %s/%s. Retrying in %s seconds. Error: %s",
            job.id,
            job.attempts,
            job.max_attempts,
            delay,
            error_message,
        )

        raise self.retry(exc=exc, countdown=delay)


@shared_task
def process_high_priority_email(job_id):
    return process_email_job(job_id)


@shared_task
def process_due_email_jobs(batch_size=100):
    now = timezone.now()

    due_jobs = (
        EmailJob.objects
        .filter(status="queued", scheduled_at__lte=now)
        .filter(next_retry_at__isnull=True)
        .order_by("-priority", "scheduled_at")[:batch_size]
    )

    delayed_retry_jobs = (
        EmailJob.objects
        .filter(status="queued", scheduled_at__lte=now, next_retry_at__lte=now)
        .order_by("-priority", "next_retry_at")[:batch_size]
    )

    job_ids = list(due_jobs.values_list("id", "priority", "email_type"))
    retry_job_ids = list(delayed_retry_jobs.values_list("id", "priority", "email_type"))

    combined = []
    seen = set()

    for row in job_ids + retry_job_ids:
        if row[0] in seen:
            continue
        combined.append(row)
        seen.add(row[0])

    dispatched = 0

    for job_id, priority, email_type in combined:
        if priority >= 8 or email_type == "otp":
            process_high_priority_email.delay(job_id)
        else:
            process_email_job.delay(job_id)

        dispatched += 1

    logger.info("Dispatched %s due email jobs.", dispatched)
    return {"dispatched": dispatched}


@shared_task
def reset_smtp_minute_counters():
    now = timezone.now()

    updated = SMTPConfig.objects.update(
        sent_this_minute=0,
        last_minute_reset_at=now,
    )

    logger.info("Reset minute counters for %s SMTP configs.", updated)
    return {"reset_count": updated}


@shared_task
def reset_smtp_hourly_counters():
    now = timezone.now()

    updated = SMTPConfig.objects.update(
        sent_this_hour=0,
        last_hourly_reset_at=now,
    )

    logger.info("Reset hourly counters for %s SMTP configs.", updated)
    return {"reset_count": updated}


@shared_task
def reset_smtp_daily_counters():
    now = timezone.now()

    updated = SMTPConfig.objects.update(
        sent_today=0,
        sent_this_hour=0,
        sent_this_minute=0,
        last_reset_at=now,
        last_hourly_reset_at=now,
        last_minute_reset_at=now,
    )

    logger.info("Reset daily counters for %s SMTP configs.", updated)
    return {"reset_count": updated}


@shared_task
def retry_failed_jobs(batch_size=100):
    jobs = (
        EmailJob.objects
        .filter(status="failed", attempts__lt=F("max_attempts"))
        .order_by("-priority", "id")[:batch_size]
    )

    count = 0

    for job in jobs:
        job.status = "queued"
        job.next_retry_at = timezone.now()
        job.save(update_fields=["status", "next_retry_at"])
        count += 1

    logger.info("Re-queued %s failed email jobs.", count)
    return {"retried_count": count}


@shared_task
def check_smtp_health(batch_size=50):
    configs = (
        SMTPConfig.objects
        .filter(is_active=True)
        .order_by("last_tested_at", "id")[:batch_size]
    )

    checked = 0
    failed = 0

    for config in configs:
        success, message = EmailService.test_smtp_connection(config)

        checked += 1
        if not success:
            failed += 1
            logger.warning("SMTP health check failed for %s: %s", config.id, message)

    return {
        "checked": checked,
        "failed": failed,
    }


@shared_task
def cleanup_old_email_jobs(days=90):
    cutoff = timezone.now() - timedelta(days=days)

    deleted, _ = EmailJob.objects.filter(
        status__in=["done", "cancelled"],
        id__isnull=False,
    ).delete()

    logger.info("Cleaned up %s old completed/cancelled email job records.", deleted)
    return {"deleted": deleted}


@shared_task
def cleanup_old_email_jobs_including_failed(days=180):
    cutoff = timezone.now() - timedelta(days=days)

    deleted, _ = EmailJob.objects.filter(
        status__in=["done", "cancelled", "failed"],
        id__isnull=False,
    ).delete()

    logger.info("Cleaned up %s old email job records including failed.", deleted)
    return {"deleted": deleted}
