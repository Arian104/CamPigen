from django.contrib import admin
from .models import TrackedLink, LinkClick


@admin.register(TrackedLink)
class TrackedLinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "original_url",
        "tracking_code",
        "is_active",
        "click_count",
        "unique_click_count",
        "last_clicked_at",
    )
    list_filter = ("organization", "is_active")
    search_fields = ("name", "original_url", "tracking_code")
    readonly_fields = (
        "id",
        "tracking_code",
        "click_count",
        "unique_click_count",
        "last_clicked_at",
    )


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = (
        "tracked_link",
        "organization",
        "contact",
        "ip_address",
        "device_type",
        "browser",
        "is_unique",
        "clicked_at",
    )
    list_filter = ("organization", "device_type", "browser", "is_unique")
    search_fields = (
        "tracked_link__name",
        "tracked_link__original_url",
        "ip_address",
        "user_agent",
    )
    readonly_fields = ("id", "clicked_at")
