from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from ..models import SMTPConfig
from .health import SMTPHealthService


class SMTPRouter:
    @staticmethod
    def is_rate_limited(smtp_config: SMTPConfig) -> bool:
        if smtp_config.daily_limit and smtp_config.sent_today >= smtp_config.daily_limit:
            return True
        if smtp_config.hourly_limit and smtp_config.sent_this_hour >= smtp_config.hourly_limit:
            return True
        if smtp_config.minute_limit and smtp_config.sent_this_minute >= smtp_config.minute_limit:
            return True
        return False

    @staticmethod
    def is_email_type_allowed(smtp_config: SMTPConfig, email_type: str) -> bool:
        allowed = smtp_config.allowed_email_types or []
        if not allowed:
            return True
        return email_type in allowed

    @staticmethod
    def is_domain_allowed(smtp_config: SMTPConfig, recipient_email: str) -> bool:
        allowed = smtp_config.allowed_domains or []
        if not allowed:
            return True

        domain = recipient_email.split("@")[-1].lower()
        return domain in [item.lower() for item in allowed]

    @classmethod
    def select_smtp(cls, organization, email_type="custom", priority=5, recipient_email=""):
        if not organization:
            return None

        now = timezone.now()

        candidates = SMTPConfig.objects.filter(
            organization=organization,
            is_active=True,
        ).filter(
            Q(cooldown_until__isnull=True) | Q(cooldown_until__lte=now)
        )

        filtered_ids = []

        for smtp in candidates:
            if cls.is_rate_limited(smtp):
                continue
            if not cls.is_email_type_allowed(smtp, email_type):
                continue
            if recipient_email and not cls.is_domain_allowed(smtp, recipient_email):
                continue
            filtered_ids.append(smtp.id)

        if not filtered_ids:
            return None

        with transaction.atomic():
            smtp = (
                SMTPConfig.objects.select_for_update(skip_locked=True)
                .filter(id__in=filtered_ids)
                .order_by(
                    "priority",
                    "-health_score",
                    "sent_today",
                    "sent_this_hour",
                    "sent_this_minute",
                    "last_used_at",
                )
                .first()
            )

            if not smtp:
                return None

            if cls.is_rate_limited(smtp):
                return None

            return smtp

    @staticmethod
    def record_success(smtp_config: SMTPConfig):
        SMTPHealthService.record_success(smtp_config)

    @staticmethod
    def record_failure(smtp_config: SMTPConfig, error_message: str = ""):
        SMTPHealthService.record_failure(smtp_config, error_message)
