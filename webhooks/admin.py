from django.contrib import admin
from .models import Webhook, WebhookDelivery


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "organization",
        "is_active",
        "last_triggered_at",
        "created_at",
    )
    list_filter = ("organization", "is_active")
    search_fields = ("name", "url")
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "last_triggered_at",
        "last_success_at",
        "last_failure_at",
    )
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "url", "organization", "is_active"),
        }),
        ("Events & Security", {
            "fields": ("events", "secret_key", "custom_headers"),
        }),
        ("Retry Configuration", {
            "fields": ("retry_count", "retry_delay", "timeout_seconds"),
        }),
        ("Status", {
            "fields": ("last_triggered_at", "last_success_at", "last_failure_at"),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("created_by", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "webhook",
        "event_type",
        "success",
        "response_status",
        "attempts",
        "created_at",
    )
    list_filter = ("success", "event_type", "webhook")
    search_fields = ("webhook__name", "webhook__url", "error_message")
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "request_headers",
        "response_body",
        "error_message",
    )
