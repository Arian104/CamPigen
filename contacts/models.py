import uuid
from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel


class Contact(TimeStampedModel):
    LIFECYCLE_CHOICES = [
        ("subscriber", "Subscriber"),
        ("lead_new", "New Lead"),
        ("lead_warm", "Warm Lead"),
        ("lead_hot", "Hot Lead"),
        ("customer", "Customer"),
        ("inactive", "Inactive"),
        ("churn_risk", "Churn Risk"),
    ]

    CONSENT_CHOICES = [
        ("unknown", "Unknown"),
        ("subscribed", "Subscribed"),
        ("unsubscribed", "Unsubscribed"),
        ("bounced", "Bounced"),
        ("complained", "Complained"),
        ("suppressed", "Suppressed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contacts",
    )

    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)

    phone = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    timezone = models.CharField(max_length=80, blank=True)
    language = models.CharField(max_length=20, blank=True)

    source = models.CharField(max_length=120, blank=True)
    source_detail = models.CharField(max_length=255, blank=True)

    lifecycle_stage = models.CharField(
        max_length=40,
        choices=LIFECYCLE_CHOICES,
        default="subscriber",
        db_index=True,
    )

    lead_score = models.IntegerField(default=0, db_index=True)
    engagement_score = models.IntegerField(default=0, db_index=True)

    consent_status = models.CharField(
        max_length=40,
        choices=CONSENT_CHOICES,
        default="unknown",
        db_index=True,
    )

    is_unsubscribed = models.BooleanField(default=False, db_index=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, editable=False)

    email_verified = models.BooleanField(default=False)
    email_status = models.CharField(max_length=50, blank=True)

    last_emailed_at = models.DateTimeField(null=True, blank=True)
    last_opened_at = models.DateTimeField(null=True, blank=True)
    last_clicked_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)

    custom_fields = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = [("organization", "email")]
        indexes = [
            models.Index(fields=["organization", "email"]),
            models.Index(fields=["organization", "is_unsubscribed"]),
            models.Index(fields=["organization", "consent_status"]),
            models.Index(fields=["organization", "lifecycle_stage"]),
            models.Index(fields=["organization", "lead_score"]),
            models.Index(fields=["organization", "engagement_score"]),
            models.Index(fields=["organization", "country"]),
            models.Index(fields=["organization", "source"]),
            models.Index(fields=["last_emailed_at"]),
            models.Index(fields=["last_opened_at"]),
            models.Index(fields=["last_clicked_at"]),
        ]
        ordering = ["-created_at"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_global(self):
        return self.organization is None

    def mark_activity(self):
        self.last_activity_at = timezone.now()
        self.save(update_fields=["last_activity_at", "updated_at"])

    def __str__(self):
        org_name = self.organization.name if self.organization else "Global"
        return f"{self.email} ({org_name})"


class ContactFieldDefinition(TimeStampedModel):
    FIELD_TYPES = [
        ("text", "Text"),
        ("textarea", "Textarea"),
        ("number", "Number"),
        ("decimal", "Decimal"),
        ("date", "Date"),
        ("datetime", "DateTime"),
        ("boolean", "Boolean"),
        ("select", "Select"),
        ("multi_select", "Multi Select"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("url", "URL"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="contact_field_definitions",
    )

    field_key = models.SlugField(max_length=100)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=30, choices=FIELD_TYPES, default="text")

    options = models.JSONField(default=list, blank=True)
    default_value = models.CharField(max_length=255, blank=True)

    is_required = models.BooleanField(default=False)
    is_filterable = models.BooleanField(default=True)
    is_visible_in_table = models.BooleanField(default=True)
    is_importable = models.BooleanField(default=True)

    help_text = models.CharField(max_length=255, blank=True)
    placeholder = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("organization", "field_key")]
        ordering = ["order", "label"]
        indexes = [
            models.Index(fields=["organization", "field_key"]),
            models.Index(fields=["organization", "is_active"]),
            models.Index(fields=["organization", "is_filterable"]),
        ]

    def __str__(self):
        return f"{self.organization.name} - {self.label}"


class Tag(TimeStampedModel):
    TAG_TYPES = [
        ("source", "Source"),
        ("lifecycle", "Lifecycle"),
        ("interest", "Interest"),
        ("behavior", "Behavior"),
        ("campaign", "Campaign"),
        ("suppression", "Suppression"),
        ("value", "Value"),
        ("geo", "Geo"),
        ("custom", "Custom"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tags",
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    tag_type = models.CharField(max_length=30, choices=TAG_TYPES, default="custom")
    color = models.CharField(max_length=20, default="#2563eb")
    description = models.TextField(blank=True)

    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("organization", "slug")]
        ordering = ["tag_type", "name"]
        indexes = [
            models.Index(fields=["organization", "slug"]),
            models.Index(fields=["organization", "tag_type"]),
            models.Index(fields=["organization", "is_active"]),
        ]

    def __str__(self):
        org_name = self.organization.name if self.organization else "Global"
        return f"{self.name} ({org_name})"


class ContactTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="contact_tags",
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="contact_tags",
    )

    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [("contact", "tag")]
        indexes = [
            models.Index(fields=["contact", "tag"]),
            models.Index(fields=["tag"]),
        ]

    def __str__(self):
        return f"{self.contact.email} - {self.tag.name}"


class ContactList(TimeStampedModel):
    LIST_TYPES = [
        ("static", "Static List"),
        ("dynamic", "Dynamic Segment"),
        ("suppression", "Suppression List"),
        ("seed", "Seed List"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contact_lists",
    )

    name = models.CharField(max_length=255)
    list_type = models.CharField(max_length=30, choices=LIST_TYPES, default="static")
    description = models.TextField(blank=True)

    filter_criteria = models.JSONField(default=dict, blank=True)

    total_contacts = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_contact_lists",
    )

    class Meta:
        unique_together = [("organization", "name")]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "list_type"]),
            models.Index(fields=["organization", "is_active"]),
        ]

    def __str__(self):
        org_name = self.organization.name if self.organization else "Global"
        return f"{self.name} ({org_name})"


class ContactListMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="list_memberships",
    )

    contact_list = models.ForeignKey(
        ContactList,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [("contact", "contact_list")]
        indexes = [
            models.Index(fields=["contact", "contact_list"]),
            models.Index(fields=["contact_list"]),
        ]

    def __str__(self):
        return f"{self.contact.email} in {self.contact_list.name}"


class ContactImportBatch(TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("partially_completed", "Partially Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="contact_import_batches",
    )

    uploaded_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    file_name = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=120, blank=True)

    column_mapping = models.JSONField(default=dict, blank=True)

    total_rows = models.PositiveIntegerField(default=0)
    successful_rows = models.PositiveIntegerField(default=0)
    failed_rows = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    error_report = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "created_at"]),
        ]

    def __str__(self):
        return f"{self.file_name or self.id} - {self.status}"


class ContactActivity(TimeStampedModel):
    ACTIVITY_TYPES = [
        ("created", "Created"),
        ("updated", "Updated"),
        ("tag_added", "Tag Added"),
        ("tag_removed", "Tag Removed"),
        ("list_added", "Added To List"),
        ("list_removed", "Removed From List"),
        ("email_sent", "Email Sent"),
        ("email_opened", "Email Opened"),
        ("email_clicked", "Email Clicked"),
        ("email_bounced", "Email Bounced"),
        ("unsubscribed", "Unsubscribed"),
        ("complained", "Complained"),
        ("custom", "Custom"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="contact_activities",
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    activity_type = models.CharField(max_length=40, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    email_job = models.ForeignKey(
        "email_engine.EmailJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "activity_type"]),
            models.Index(fields=["contact", "activity_type"]),
            models.Index(fields=["contact", "created_at"]),
        ]

    def __str__(self):
        return f"{self.contact.email} - {self.activity_type}"
