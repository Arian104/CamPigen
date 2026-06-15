import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel


def user_avatar_upload_path(instance, filename):
    return f"users/avatars/{instance.id}/{filename}"


class User(AbstractUser, TimeStampedModel):
    """
    Core user model for multi-tenant SaaS platform.
    Handles identity, user preferences, active organization, and security metadata.
    """

    THEME_CHOICES = [
        ("system", "System"),
        ("light", "Light"),
        ("dark", "Dark"),
    ]

    TIME_FORMAT_CHOICES = [
        ("12h", "12 Hour"),
        ("24h", "24 Hour"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True)

    phone = models.CharField(max_length=20, blank=True, default="")
    display_name = models.CharField(max_length=255, blank=True, default="")
    job_title = models.CharField(max_length=255, blank=True, default="")
    department = models.CharField(max_length=255, blank=True, default="")

    avatar = models.ImageField(upload_to=user_avatar_upload_path, null=True, blank=True)
    avatar_url = models.URLField(blank=True, default="")

    email_verified = models.BooleanField(default=False)

    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=64, blank=True, default="")

    active_organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_users",
    )

    timezone = models.CharField(max_length=64, default="Asia/Dhaka")
    language = models.CharField(max_length=20, default="en")
    date_format = models.CharField(max_length=50, default="MMM D, YYYY")
    time_format = models.CharField(max_length=10, choices=TIME_FORMAT_CHOICES, default="12h")

    theme_mode = models.CharField(max_length=20, choices=THEME_CHOICES, default="system")
    accent_color = models.CharField(max_length=20, default="#4f46e5")
    sidebar_collapsed = models.BooleanField(default=False)
    default_dashboard = models.CharField(max_length=100, default="/")

    preferences = models.JSONField(default=dict, blank=True)
    notification_preferences = models.JSONField(default=dict, blank=True)

    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    password_changed_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.TextField(blank=True, default="")
    last_seen_at = models.DateTimeField(null=True, blank=True)

    is_system_user = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def avatar_display_url(self):
        if self.avatar:
            return self.avatar.url
        return self.avatar_url

    @property
    def is_locked(self):
        return bool(self.locked_until and self.locked_until > timezone.now())

    def get_organizations(self):
        return [membership.organization for membership in self.organization_memberships.all()]

    def has_org_role(self, organization, roles):
        return self.organization_memberships.filter(
            organization=organization,
            role__in=roles,
        ).exists()

    def get_active_organization(self):
        return self.active_organization


class EmailVerificationToken(TimeStampedModel):
    """
    Stores hashed email verification tokens.
    Never store raw tokens in the database.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="email_verification_tokens",
    )

    email = models.EmailField()
    token_hash = models.CharField(max_length=128, db_index=True)

    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["user", "token_hash"]),
            models.Index(fields=["expires_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Email verification for {self.email}"

    @property
    def is_used(self):
        return self.used_at is not None

    @property
    def is_expired(self):
        return self.expires_at <= timezone.now()

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired


class PasswordResetToken(TimeStampedModel):
    """
    Stores hashed password reset tokens.
    Never store raw tokens in the database.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )

    token_hash = models.CharField(max_length=128, db_index=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["user", "token_hash"]),
            models.Index(fields=["expires_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Password reset for {self.user.email}"

    @property
    def is_used(self):
        return self.used_at is not None

    @property
    def is_expired(self):
        return self.expires_at <= timezone.now()

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired


class UserSession(TimeStampedModel):
    """
    Tracks user login sessions for security and audit.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    session_key = models.CharField(max_length=128, blank=True, default="", db_index=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")

    device_name = models.CharField(max_length=255, blank=True, default="")
    browser = models.CharField(max_length=100, blank=True, default="")
    os = models.CharField(max_length=100, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")

    is_active = models.BooleanField(default=True)
    last_activity_at = models.DateTimeField(auto_now=True)

    revoked_at = models.DateTimeField(null=True, blank=True)
    revoked_reason = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["session_key"]),
            models.Index(fields=["last_activity_at"]),
        ]
        ordering = ["-last_activity_at"]

    def __str__(self):
        return f"{self.user.email} session"

    def revoke(self, reason=""):
        self.is_active = False
        self.revoked_at = timezone.now()
        self.revoked_reason = reason
        self.save(update_fields=["is_active", "revoked_at", "revoked_reason"])


class UserActivityLog(TimeStampedModel):
    """
    Audit log for user actions.
    """

    ACTION_CHOICES = [
        ("register", "Register"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("verify_email", "Verify Email"),
        ("request_password_reset", "Request Password Reset"),
        ("reset_password", "Reset Password"),
        ("change_password", "Change Password"),
        ("update_profile", "Update Profile"),
        ("upload_avatar", "Upload Avatar"),
        ("remove_avatar", "Remove Avatar"),
        ("switch_org", "Switch Organization"),
        ("mfa_enabled", "MFA Enabled"),
        ("mfa_disabled", "MFA Disabled"),
        ("session_revoked", "Session Revoked"),
        ("organization_updated", "Organization Updated"),
        ("organization_logo_updated", "Organization Logo Updated"),
        ("organization_branding_updated", "Organization Branding Updated"),
        ("delete", "Delete"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="activity_logs",
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(max_length=80, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["user", "action"]),
            models.Index(fields=["organization", "created_at"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.action}"
