from django.db import models
from core.models import TimeStampedModel


class OrganizationAnalytics(TimeStampedModel):
    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="analytics",
    )

    total_campaigns = models.PositiveIntegerField(default=0)
    total_contacts = models.PositiveIntegerField(default=0)

    total_email_jobs = models.PositiveIntegerField(default=0)
    total_emails_sent = models.PositiveIntegerField(default=0)
    total_emails_failed = models.PositiveIntegerField(default=0)
    total_emails_queued = models.PositiveIntegerField(default=0)

    total_generated_links = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    total_unique_clicks = models.PositiveIntegerField(default=0)
    total_clicked_contacts = models.PositiveIntegerField(default=0)

    total_webhook_deliveries = models.PositiveIntegerField(default=0)
    total_webhook_success = models.PositiveIntegerField(default=0)
    total_webhook_failures = models.PositiveIntegerField(default=0)

    last_email_sent_at = models.DateTimeField(null=True, blank=True)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    last_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Organization Analytics"

    def __str__(self):
        return f"Analytics for {self.organization.name}"


class CampaignAnalytics(TimeStampedModel):
    campaign = models.OneToOneField(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        related_name="analytics",
    )

    total_jobs = models.PositiveIntegerField(default=0)
    total_queued = models.PositiveIntegerField(default=0)
    total_processing = models.PositiveIntegerField(default=0)
    total_sent = models.PositiveIntegerField(default=0)
    total_failed = models.PositiveIntegerField(default=0)

    total_delivered = models.PositiveIntegerField(default=0)
    total_opens = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    unique_clicks = models.PositiveIntegerField(default=0)
    clicked_contacts = models.PositiveIntegerField(default=0)

    total_bounces = models.PositiveIntegerField(default=0)
    total_unsubscribes = models.PositiveIntegerField(default=0)
    total_complaints = models.PositiveIntegerField(default=0)

    recipient_count = models.PositiveIntegerField(default=0)
    generated_links = models.PositiveIntegerField(default=0)

    open_rate = models.FloatField(default=0.0)
    click_rate = models.FloatField(default=0.0)
    unique_click_rate = models.FloatField(default=0.0)
    bounce_rate = models.FloatField(default=0.0)

    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    top_clicked_url = models.URLField(max_length=1200, blank=True, default="")
    last_sent_at = models.DateTimeField(null=True, blank=True)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    last_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Campaign Analytics"

    def __str__(self):
        return f"Analytics for {self.campaign.name}"


class DailyAnalytics(TimeStampedModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="daily_analytics",
    )
    date = models.DateField(db_index=True)

    active_campaigns = models.PositiveIntegerField(default=0)
    new_contacts = models.PositiveIntegerField(default=0)

    email_jobs = models.PositiveIntegerField(default=0)
    emails_sent = models.PositiveIntegerField(default=0)
    emails_failed = models.PositiveIntegerField(default=0)
    emails_queued = models.PositiveIntegerField(default=0)
    emails_delivered = models.PositiveIntegerField(default=0)

    opens = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    unique_clicks = models.PositiveIntegerField(default=0)
    clicked_contacts = models.PositiveIntegerField(default=0)

    bounces = models.PositiveIntegerField(default=0)
    unsubscribes = models.PositiveIntegerField(default=0)

    generated_links = models.PositiveIntegerField(default=0)
    webhook_deliveries = models.PositiveIntegerField(default=0)
    webhook_failures = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("organization", "date")]
        indexes = [
            models.Index(fields=["organization", "date"]),
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.organization.name} - {self.date}"


class LinkAnalytics(TimeStampedModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="link_analytics",
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="link_analytics",
    )

    original_url = models.URLField(max_length=1200)

    generated_links = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    unique_clicks = models.PositiveIntegerField(default=0)
    clicked_contacts = models.PositiveIntegerField(default=0)

    last_clicked_at = models.DateTimeField(null=True, blank=True)
    last_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("organization", "campaign", "original_url")]
        indexes = [
            models.Index(fields=["organization", "campaign"]),
            models.Index(fields=["organization", "original_url"]),
            models.Index(fields=["last_clicked_at"]),
        ]
        ordering = ["-total_clicks", "-last_clicked_at"]

    def __str__(self):
        campaign_name = self.campaign.name if self.campaign else "Manual / No Campaign"
        return f"{campaign_name} - {self.original_url}"
