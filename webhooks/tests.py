from datetime import timedelta
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone

from email_engine.models import EmailJob
from events.models import EmailEvent
from organizations.models import Organization
from .models import Webhook, WebhookDelivery
from .tasks import retry_failed_webhooks


User = get_user_model()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class WebhookDispatchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="password123",
        )
        self.organization = Organization.objects.create(
            name="Acme Inc",
            subdomain="acme-inc",
            owner=self.user,
        )
        self.user.organization = self.organization
        self.user.save(update_fields=["organization"])

    def _create_email_job(self):
        return EmailJob.objects.create(
            organization=self.organization,
            recipient_email="recipient@example.com",
            subject_snapshot="Subject",
            body_snapshot="Body",
            scheduled_at=timezone.now(),
            status="done",
        )

    @patch("webhooks.services.requests.post")
    def test_email_event_triggers_webhook_delivery(self, mock_post):
        mock_response = Mock(status_code=200, text="ok")
        mock_post.return_value = mock_response

        webhook = Webhook.objects.create(
            organization=self.organization,
            url="https://example.com/webhook",
            events=["email.opened"],
            is_active=True,
            retry_count=3,
            retry_delay=10,
        )
        email_job = self._create_email_job()

        EmailEvent.objects.create(email_job=email_job, event_type="opened")

        delivery = WebhookDelivery.objects.get(webhook=webhook)
        self.assertTrue(delivery.success)
        self.assertEqual(delivery.response_status, 200)
        self.assertEqual(delivery.event_type, "email.opened")
        self.assertEqual(delivery.attempts, 1)

    @patch("webhooks.tasks.deliver_webhook.delay")
    def test_retry_failed_webhooks_task_queues_due_deliveries(self, mock_delay):
        webhook = Webhook.objects.create(
            organization=self.organization,
            url="https://example.com/webhook",
            events=["email.opened"],
            is_active=True,
            retry_count=3,
            retry_delay=1,
        )
        delivery = WebhookDelivery.objects.create(
            webhook=webhook,
            event=None,
            event_type="email.opened",
            payload={"test": True},
            success=False,
            attempts=1,
            max_attempts=3,
            next_retry_at=timezone.now() - timedelta(seconds=1),
        )

        result = retry_failed_webhooks()
        self.assertIn("retried_count", result)
        self.assertEqual(result["retried_count"], 1)
        mock_delay.assert_called_once_with(str(delivery.id))
