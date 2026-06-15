from django.contrib import admin
from .models import (
    OrganizationAnalytics,
    CampaignAnalytics,
    DailyAnalytics,
    LinkAnalytics,
)


@admin.register(OrganizationAnalytics)
class OrganizationAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "total_campaigns",
        "total_contacts",
        "total_emails_sent",
        "total_clicks",
        "total_webhook_deliveries",
        "last_updated_at",
    )
    readonly_fields = ("created_at", "updated_at", "last_updated_at")


@admin.register(CampaignAnalytics)
class CampaignAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "campaign",
        "total_sent",
        "total_failed",
        "total_clicks",
        "unique_clicks",
        "click_rate",
        "last_updated_at",
    )
    readonly_fields = ("created_at", "updated_at", "last_updated_at")


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "date",
        "emails_sent",
        "emails_failed",
        "clicks",
        "unique_clicks",
        "webhook_deliveries",
    )
    list_filter = ("organization", "date")
    readonly_fields = ("created_at", "updated_at")


@admin.register(LinkAnalytics)
class LinkAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "campaign",
        "original_url",
        "generated_links",
        "total_clicks",
        "unique_clicks",
        "clicked_contacts",
        "last_clicked_at",
    )
    list_filter = ("organization", "campaign")
    search_fields = ("original_url", "campaign__name")
    readonly_fields = ("created_at", "updated_at", "last_updated_at")
