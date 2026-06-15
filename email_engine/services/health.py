from datetime import timedelta
from django.utils import timezone


class SMTPHealthService:
    @staticmethod
    def record_success(smtp_config):
        smtp_config.success_count += 1
        smtp_config.failure_count = 0
        smtp_config.last_success_at = timezone.now()
        smtp_config.last_used_at = timezone.now()
        smtp_config.cooldown_until = None
        smtp_config.health_score = min(float(smtp_config.health_score) + 2.0, 100.0)
        smtp_config.sent_today += 1
        smtp_config.sent_this_hour += 1
        smtp_config.sent_this_minute += 1
        smtp_config.save(update_fields=["success_count", "failure_count", "last_success_at", "last_used_at", "cooldown_until", "health_score", "sent_today", "sent_this_hour", "sent_this_minute"])

    @staticmethod
    def record_failure(smtp_config, error_message: str = ""):
        smtp_config.failure_count += 1
        smtp_config.last_failed_at = timezone.now()
        smtp_config.last_used_at = timezone.now()
        smtp_config.health_score = max(float(smtp_config.health_score) - 8.0, 0.0)

        if smtp_config.failure_count >= smtp_config.max_failures_before_cooldown:
            smtp_config.cooldown_until = timezone.now() + timedelta(
                minutes=smtp_config.cooldown_minutes
            )

        smtp_config.last_test_message = error_message[:1000] if error_message else smtp_config.last_test_message
        smtp_config.save(update_fields=["failure_count", "last_failed_at", "last_used_at", "health_score", "cooldown_until", "last_test_message"])


class SMTPHealthChecker:
    @staticmethod
    def update_health_score(config, success):
        if success:
            SMTPHealthService.record_success(config)
        else:
            SMTPHealthService.record_failure(config, "SMTP health check failed.")
