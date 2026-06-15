import uuid
from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel

User = get_user_model()


class Organization(TimeStampedModel):
    PLAN_CHOICES = [
        ("free", "Free"),
        ("pro", "Professional"),
        ("enterprise", "Enterprise"),
    ]

    INDUSTRY_CHOICES = [
        ("custom", "Custom"),
        ("restaurant", "Restaurant"),
        ("cafe", "Cafe"),
        ("gym", "Gym"),
        ("education", "Education"),
        ("visa_consultant", "Visa Consultant"),
        ("ecommerce", "Ecommerce"),
        ("online_course", "Online Course"),
        ("agency", "Agency"),
        ("saas", "SaaS"),
    ]

    UNSUBSCRIBE_POLICY_CHOICES = [
        ("one_click", "One Click"),
        ("confirmation", "Confirmation Page"),
        ("preference_center", "Preference Center"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Core tenant identity
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=100, unique=True, db_index=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    industry_type = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, default="custom")
    website = models.URLField(blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")
    timezone = models.CharField(max_length=100, default="Asia/Dhaka")
    is_active = models.BooleanField(default=True)

    # Ownership
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_organizations",
    )

    # Brand identity
    brand_name = models.CharField(max_length=255, blank=True, default="")
    logo = models.ImageField(upload_to="organization/logos/", blank=True, null=True)
    favicon = models.ImageField(upload_to="organization/favicons/", blank=True, null=True)
    primary_color = models.CharField(max_length=20, default="#2563eb")
    secondary_color = models.CharField(max_length=20, default="#111827")
    accent_color = models.CharField(max_length=20, default="#10b981")
    font_family = models.CharField(max_length=100, default="Inter")
    button_style = models.CharField(max_length=50, default="rounded")

    # Campaign/template defaults, not SMTP routing
    default_from_name = models.CharField(max_length=255, blank=True, default="")
    default_from_email = models.EmailField(blank=True, default="")
    default_reply_to_email = models.EmailField(blank=True, default="")
    default_campaign_language = models.CharField(max_length=20, default="en")
    default_footer_text = models.TextField(blank=True, default="")
    default_disclaimer = models.TextField(blank=True, default="")
    default_email_theme = models.JSONField(default=dict, blank=True)
    default_template_width = models.PositiveIntegerField(default=600)
    default_header_logo_enabled = models.BooleanField(default=True)
    default_footer_enabled = models.BooleanField(default=True)

    # Business/compliance profile
    company_legal_name = models.CharField(max_length=255, blank=True, default="")
    business_phone = models.CharField(max_length=50, blank=True, default="")
    support_email = models.EmailField(blank=True, default="")
    business_address = models.TextField(blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    postal_code = models.CharField(max_length=50, blank=True, default="")

    unsubscribe_policy = models.CharField(
        max_length=50,
        choices=UNSUBSCRIBE_POLICY_CHOICES,
        default="one_click",
    )
    physical_address_required = models.BooleanField(default=True)
    gdpr_enabled = models.BooleanField(default=False)
    double_opt_in_enabled = models.BooleanField(default=False)
    marketing_consent_required = models.BooleanField(default=True)

    # CDP preset control
    contact_schema_preset = models.CharField(max_length=50, default="custom")
    preset_applied = models.BooleanField(default=False)
    preset_applied_at = models.DateTimeField(null=True, blank=True)

    # Social/public links
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    tiktok_url = models.URLField(blank=True, default="")
    whatsapp_number = models.CharField(max_length=50, blank=True, default="")

    # Plan/feature access
    max_users = models.PositiveIntegerField(default=3)
    max_contacts = models.PositiveIntegerField(default=1000)
    max_templates = models.PositiveIntegerField(default=20)
    max_segments = models.PositiveIntegerField(default=10)
    automation_enabled = models.BooleanField(default=False)
    advanced_segmentation_enabled = models.BooleanField(default=False)
    webhooks_enabled = models.BooleanField(default=False)
    ai_features_enabled = models.BooleanField(default=False)
    custom_branding_enabled = models.BooleanField(default=False)

    # Flexible future-safe settings
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["subdomain"]),
            models.Index(fields=["plan", "is_active"]),
            models.Index(fields=["industry_type"]),
        ]

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return self.brand_name or self.name

    def get_template_variables(self):
        return {
            "organization": {
                "id": str(self.id),
                "name": self.name,
                "brand_name": self.display_name,
                "website": self.website,
                "logo_url": self.logo.url if self.logo else "",
                "primary_color": self.primary_color,
                "secondary_color": self.secondary_color,
                "accent_color": self.accent_color,
                "support_email": self.support_email,
                "business_phone": self.business_phone,
                "business_address": self.business_address,
                "city": self.city,
                "state": self.state,
                "postal_code": self.postal_code,
                "country": self.country,
                "legal_name": self.company_legal_name,
                "facebook_url": self.facebook_url,
                "instagram_url": self.instagram_url,
                "linkedin_url": self.linkedin_url,
                "twitter_url": self.twitter_url,
                "youtube_url": self.youtube_url,
                "tiktok_url": self.tiktok_url,
                "whatsapp_number": self.whatsapp_number,
            }
        }


class OrganizationMembership(TimeStampedModel):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Administrator"),
        ("manager", "Manager"),
        ("marketer", "Marketer"),
        ("analyst", "Analyst"),
        ("viewer", "Viewer"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("invited", "Invited"),
        ("suspended", "Suspended"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organization_memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_organization_invites",
    )
    joined_at = models.DateTimeField(null=True, blank=True)
    last_active_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("user", "organization")]
        indexes = [
            models.Index(fields=["user", "organization"]),
            models.Index(fields=["organization", "role"]),
            models.Index(fields=["organization", "status"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"
