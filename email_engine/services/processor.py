import time

from django.utils import timezone

from ..models import SMTPDeliveryAttempt
from .email_service import EmailService
from .router import SMTPRouter


class EmailJobProcessor:
    @staticmethod
    def process(job):
        organization = job.organization or (job.campaign.organization if job.campaign else None)

        if not organization:
            raise Exception("Email job has no organization.")

        if job.use_custom_smtp and job.custom_smtp_config:
            smtp_config = job.custom_smtp_config

            if not smtp_config.is_active:
                raise Exception("Selected SMTP configuration is inactive.")
        else:
            smtp_config = SMTPRouter.select_smtp(
                organization=organization,
                email_type=job.email_type,
                priority=job.priority,
                recipient_email=job.recipient_email,
            )

        if not smtp_config:
            raise Exception(
                "No available SMTP configuration. All SMTPs may be inactive, cooling down, or rate limited."
            )

        attempt_number = job.attempts + 1
        started_at = timezone.now()
        start = time.monotonic()

        attempt = SMTPDeliveryAttempt.objects.create(
            email_job=job,
            smtp_config=smtp_config,
            organization=organization,
            attempt_number=attempt_number,
            status="started",
            started_at=started_at,
        )

        success, message = EmailService.send_with_custom_smtp(job, smtp_config)

        finished_at = timezone.now()
        latency_ms = int((time.monotonic() - start) * 1000)

        if success:
            SMTPRouter.record_success(smtp_config)

            attempt.status = "success"
            attempt.response_message = message
            attempt.finished_at = finished_at
            attempt.latency_ms = latency_ms
            attempt.save()

            job.status = "done"
            job.sent_at = timezone.now()
            job.error_message = ""
            job.last_smtp_config = smtp_config
            job.save(update_fields=["status", "sent_at", "error_message", "last_smtp_config"])

            return True, message, smtp_config

        SMTPRouter.record_failure(smtp_config, message)

        attempt.status = "failed"
        attempt.error_message = message
        attempt.finished_at = finished_at
        attempt.latency_ms = latency_ms
        attempt.save()

        job.last_smtp_config = smtp_config
        job.save(update_fields=["last_smtp_config"])

        raise Exception(message)
