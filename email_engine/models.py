from django.db import models
from core.models import TimeStampedModel, OrganizationScopedModel


class EmailJob(TimeStampedModel):
    PRIORITY_CHOICES = [(i, i) for i in range(1, 11)]

    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("processing", "Processing"),
        ("done", "Done"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    EMAIL_TYPES = [
        ("campaign", "Marketing Campaign"),
        ("transactional", "Transactional"),
        ("otp", "OTP / Verification"),
        ("notification", "System Notification"),
        ("custom", "Custom Email"),
    ]

    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        "contacts.Contact",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES, default="campaign")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=5)

    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=255, blank=True)
    recipient_phone = models.CharField(max_length=20, blank=True)

    from_email = models.EmailField(blank=True, default="")
    from_name = models.CharField(max_length=255, blank=True)
    reply_to = models.EmailField(blank=True)

    subject_snapshot = models.CharField(max_length=255)
    body_snapshot = models.TextField(default="", blank=True)
    html_body = models.TextField(blank=True)

    # Link tracking
    links_processed = models.BooleanField(default=False)

    otp_code = models.CharField(max_length=10, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    scheduled_at = models.DateTimeField(db_index=True)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    next_retry_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    use_custom_smtp = models.BooleanField(default=False)
    custom_smtp_config = models.ForeignKey(
        "SMTPConfig",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    last_smtp_config = models.ForeignKey(
        "SMTPConfig",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_used_jobs",
    )

    class Meta:
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["status", "priority", "scheduled_at"]),
            models.Index(fields=["campaign", "status"]),
            models.Index(fields=["email_type", "status"]),
            models.Index(fields=["otp_code", "otp_expires_at"]),
            models.Index(fields=["next_retry_at"]),
        ]
        ordering = ["-priority", "scheduled_at"]

    def __str__(self):
        return f"Job {self.id} - {self.recipient_email} ({self.email_type})"


class SMTPConfig(OrganizationScopedModel):
    SMTP_TYPES = [
        ("brevo", "Brevo"),
        ("gmail", "Gmail"),
        ("ses", "Amazon SES"),
        ("sendgrid", "SendGrid"),
        ("custom", "Custom"),
    ]

    name = models.CharField(max_length=255, blank=True)
    smtp_type = models.CharField(max_length=20, choices=SMTP_TYPES, default="custom")

    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=587)
    username = models.CharField(max_length=255)
    password_encrypted = models.TextField()

    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)

    from_email = models.EmailField(blank=True, default="")
    from_name = models.CharField(max_length=255, blank=True, default="")
    reply_to_email = models.EmailField(blank=True, default="")

    priority = models.SmallIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    daily_limit = models.PositiveIntegerField(default=300)
    hourly_limit = models.PositiveIntegerField(default=50)
    minute_limit = models.PositiveIntegerField(default=5)

    sent_today = models.PositiveIntegerField(default=0)
    sent_this_hour = models.PositiveIntegerField(default=0)
    sent_this_minute = models.PositiveIntegerField(default=0)

    last_reset_at = models.DateTimeField(auto_now_add=True)
    last_hourly_reset_at = models.DateTimeField(null=True, blank=True)
    last_minute_reset_at = models.DateTimeField(null=True, blank=True)

    failure_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    last_failed_at = models.DateTimeField(null=True, blank=True)
    last_success_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    health_score = models.FloatField(default=100.0)

    cooldown_until = models.DateTimeField(null=True, blank=True)
    cooldown_minutes = models.PositiveIntegerField(default=30)
    max_failures_before_cooldown = models.PositiveIntegerField(default=5)

    allowed_email_types = models.JSONField(default=list, blank=True)
    allowed_domains = models.JSONField(default=list, blank=True)

    last_tested_at = models.DateTimeField(null=True, blank=True)
    last_test_status = models.CharField(max_length=20, blank=True, default="")
    last_test_message = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["priority", "-health_score", "sent_today"]
        indexes = [
            models.Index(fields=["organization", "is_active"]),
            models.Index(fields=["organization", "is_default"]),
            models.Index(fields=["organization", "priority"]),
            models.Index(fields=["smtp_type"]),
            models.Index(fields=["cooldown_until"]),
            models.Index(fields=["health_score"]),
        ]

    def __str__(self):
        return f"{self.organization.name} - {self.name or self.host}"

    @property
    def is_in_cooldown(self):
        from django.utils import timezone

        return bool(self.cooldown_until and self.cooldown_until > timezone.now())

    @property
    def daily_remaining(self):
        if self.daily_limit == 0:
            return 999999999
        return max(self.daily_limit - self.sent_today, 0)

    @property
    def hourly_remaining(self):
        if self.hourly_limit == 0:
            return 999999999
        return max(self.hourly_limit - self.sent_this_hour, 0)

    @property
    def minute_remaining(self):
        if self.minute_limit == 0:
            return 999999999
        return max(self.minute_limit - self.sent_this_minute, 0)


class SMTPDeliveryAttempt(TimeStampedModel):
    STATUS_CHOICES = [
        ("started", "Started"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("skipped", "Skipped"),
    ]

    email_job = models.ForeignKey(
        EmailJob,
        on_delete=models.CASCADE,
        related_name="delivery_attempts",
    )
    smtp_config = models.ForeignKey(
        SMTPConfig,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="delivery_attempts",
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    attempt_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="started")

    response_message = models.TextField(blank=True, default="")
    error_message = models.TextField(blank=True, default="")

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    latency_ms = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["email_job", "attempt_number"]),
            models.Index(fields=["smtp_config", "status"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Attempt {self.attempt_number} - Job {self.email_job_id} - {self.status}"
