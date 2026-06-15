import uuid
from django.db import models
from core.models import TimeStampedModel, OrganizationScopedModel


class Webhook(OrganizationScopedModel):
    EVENT_CHOICES = [
        ("email.sent", "Email Sent"),
        ("email.failed", "Email Failed"),
        ("email.delivered", "Email Delivered"),
        ("email.opened", "Email Opened"),
        ("email.clicked", "Email Clicked"),
        ("link.clicked", "Link Clicked"),
        ("email.bounced", "Email Bounced"),
        ("campaign.completed", "Campaign Completed"),
        ("contact.created", "Contact Created"),
        ("contact.updated", "Contact Updated"),
        ("contact.unsubscribed", "Contact Unsubscribed"),
        ("smtp.failed", "SMTP Failed"),
        ("smtp.cooldown_started", "SMTP Cooldown Started"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255, blank=True, default="")
    url = models.URLField(max_length=500)
    events = models.JSONField(default=list, blank=True)

    secret_key = models.CharField(max_length=128, blank=True, default="")
    is_active = models.BooleanField(default=True)

    retry_count = models.PositiveIntegerField(default=3)
    retry_delay = models.PositiveIntegerField(default=60)
    timeout_seconds = models.PositiveIntegerField(default=10)

    custom_headers = models.JSONField(default=dict, blank=True)

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_webhooks",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_triggered_at = models.DateTimeField(null=True, blank=True)
    last_success_at = models.DateTimeField(null=True, blank=True)
    last_failure_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "is_active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["last_triggered_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name or self.url[:50]} - {self.organization.name}"


class WebhookDelivery(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    webhook = models.ForeignKey(
        Webhook,
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    event = models.ForeignKey(
        "events.EmailEvent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="webhook_deliveries",
    )

    event_type = models.CharField(max_length=80, db_index=True)
    payload = models.JSONField(default=dict)

    request_headers = models.JSONField(default=dict, blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True, default="")

    success = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)

    next_retry_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, default="")
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "event_type"]),
            models.Index(fields=["webhook", "success"]),
            models.Index(fields=["success", "next_retry_at"]),
            models.Index(fields=["event_type", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        status = "success" if self.success else "failed"
        return f"{self.webhook.name or self.webhook.url} - {self.event_type} - {status}"
