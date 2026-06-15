import uuid
from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel, OrganizationScopedModel


class TrackedLink(OrganizationScopedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.SET_NULL, null=True, blank=True, related_name="tracked_links")
    template = models.ForeignKey("campaigns.EmailTemplate", on_delete=models.SET_NULL, null=True, blank=True, related_name="tracked_links")
    email_job = models.ForeignKey("email_engine.EmailJob", on_delete=models.SET_NULL, null=True, blank=True, related_name="tracked_links")
    contact = models.ForeignKey("contacts.Contact", on_delete=models.SET_NULL, null=True, blank=True, related_name="tracked_links")

    name = models.CharField(max_length=255, blank=True, default="")
    original_url = models.URLField(max_length=1200)
    tracking_code = models.CharField(max_length=64, unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    click_count = models.PositiveIntegerField(default=0)
    unique_click_count = models.PositiveIntegerField(default=0)
    last_clicked_at = models.DateTimeField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "is_active"]),
            models.Index(fields=["tracking_code"]),
            models.Index(fields=["campaign"]),
            models.Index(fields=["email_job"]),
            models.Index(fields=["contact"]),
            models.Index(fields=["last_clicked_at"]),
        ]
        ordering = ["-last_clicked_at", "name"]

    def __str__(self):
        return self.name or self.original_url

    @property
    def is_expired(self):
        return bool(self.expires_at and self.expires_at <= timezone.now())

    @property
    def can_redirect(self):
        return self.is_active and not self.is_expired


class LinkClick(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tracked_link = models.ForeignKey(TrackedLink, on_delete=models.CASCADE, related_name="clicks")
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="link_clicks")

    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.SET_NULL, null=True, blank=True, related_name="link_clicks")
    email_job = models.ForeignKey("email_engine.EmailJob", on_delete=models.SET_NULL, null=True, blank=True, related_name="link_clicks")
    contact = models.ForeignKey("contacts.Contact", on_delete=models.SET_NULL, null=True, blank=True, related_name="link_clicks")

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    referrer = models.TextField(blank=True, default="")

    device_type = models.CharField(max_length=50, blank=True, default="")
    browser = models.CharField(max_length=100, blank=True, default="")
    os = models.CharField(max_length=100, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")

    is_unique = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    clicked_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "clicked_at"]),
            models.Index(fields=["tracked_link", "clicked_at"]),
            models.Index(fields=["campaign", "clicked_at"]),
            models.Index(fields=["email_job"]),
            models.Index(fields=["contact"]),
            models.Index(fields=["is_unique"]),
        ]
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"{self.tracked_link_id} clicked at {self.clicked_at}"
