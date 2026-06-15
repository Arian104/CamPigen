from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import (
    EmailVerificationToken,
    PasswordResetToken,
    User,
    UserActivityLog,
    UserSession,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "avatar_preview",
        "email",
        "username",
        "display_name",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "email_verified",
        "active_organization",
        "theme_mode",
        "last_seen_at",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "email_verified",
        "mfa_enabled",
        "theme_mode",
        "is_deleted",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "display_name",
        "phone",
    )

    readonly_fields = (
        "id",
        "avatar_preview",
        "date_joined",
        "last_login",
        "last_seen_at",
        "last_login_ip",
        "last_login_user_agent",
        "password_changed_at",
    )

    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profile", {
            "fields": (
                "display_name",
                "phone",
                "job_title",
                "department",
                "avatar_preview",
                "avatar",
                "avatar_url",
            )
        }),
        ("Security & Verification", {
            "fields": (
                "email_verified",
                "mfa_enabled",
                "mfa_secret",
                "failed_login_attempts",
                "locked_until",
                "password_changed_at",
                "last_login_ip",
                "last_login_user_agent",
            )
        }),
        ("Organization Context", {
            "fields": (
                "active_organization",
            )
        }),
        ("Personalization", {
            "fields": (
                "timezone",
                "language",
                "date_format",
                "time_format",
                "theme_mode",
                "accent_color",
                "sidebar_collapsed",
                "default_dashboard",
                "preferences",
                "notification_preferences",
            )
        }),
        ("System Fields", {
            "fields": (
                "is_system_user",
                "is_deleted",
                "last_seen_at",
            )
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:42px;height:42px;border-radius:50%;object-fit:cover;" />',
                obj.avatar.url,
            )
        return "-"

    avatar_preview.short_description = "Avatar"


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "expires_at", "used_at", "created_at")
    search_fields = ("user__email", "email")
    list_filter = ("used_at", "expires_at")
    readonly_fields = ("id", "token_hash", "created_at", "updated_at")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "expires_at", "used_at", "created_at")
    search_fields = ("user__email",)
    list_filter = ("used_at", "expires_at")
    readonly_fields = ("id", "token_hash", "created_at", "updated_at")


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "device_name",
        "browser",
        "os",
        "ip_address",
        "is_active",
        "last_activity_at",
        "created_at",
    )

    search_fields = ("user__email", "ip_address", "browser", "os", "device_name")
    list_filter = ("is_active", "browser", "os")
    readonly_fields = ("id", "created_at", "updated_at", "last_activity_at")


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "organization",
        "action",
        "ip_address",
        "created_at",
    )

    search_fields = ("user__email", "action", "description")
    list_filter = ("action", "organization")
    readonly_fields = ("id", "created_at", "updated_at")
