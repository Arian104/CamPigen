import smtplib
import logging
from django.utils import timezone
from ..models import SMTPConfig

logger = logging.getLogger(__name__)


class SMTPHealthChecker:
    """Health checker for SMTP configurations"""

    @staticmethod
    def test_smtp(config):
        """Test SMTP connection and authentication"""
        try:
            server = smtplib.SMTP(config.host, config.port)
            server.ehlo()
            if config.use_tls:
                server.starttls()
                server.ehlo()
            server.login(config.username, config.password_encrypted)
            server.quit()
            return True
        except Exception as e:
            logger.warning(f"SMTP health check failed for {config.host}: {str(e)}")
            return False

    @staticmethod
    def update_health_score(config, success):
        """Update health score based on success/failure"""
        if success:
            config.failure_count = 0
            config.health_score = min(100, config.health_score + 5)
        else:
            config.failure_count += 1
            config.last_failed_at = timezone.now()
            config.health_score = max(0, config.health_score - 10)

            # Auto-disable after 5 consecutive failures
            if config.failure_count >= 5:
                config.is_active = False
                logger.warning(f"SMTP {config.host} auto-disabled due to multiple failures")

        config.save()