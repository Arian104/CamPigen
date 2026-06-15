from django.contrib import admin
from .models import Organization, OrganizationMembership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "subdomain",
        "plan",
        "industry_type",
        "owner",
        "is_active",
        "created_at",
    )
    list_filter = (
        "plan",
        "industry_type",
        "is_active",
        "automation_enabled",
        "webhooks_enabled",
        "ai_features_enabled",
    )
    search_fields = (
        "name",
        "brand_name",
        "subdomain",
        "owner__email",
        "default_from_email",
        "support_email",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "preset_applied_at",
    )

    fieldsets = (
        ("Core Identity", {
            "fields": (
                "id",
                "name",
                "subdomain",
                "plan",
                "industry_type",
                "website",
                "country",
                "timezone",
                "is_active",
                "owner",
            )
        }),
        ("Branding", {
            "fields": (
                "brand_name",
                "logo",
                "favicon",
                "primary_color",
                "secondary_color",
                "accent_color",
                "font_family",
                "button_style",
            )
        }),
        ("Campaign Defaults", {
            "fields": (
                "default_from_name",
                "default_from_email",
                "default_reply_to_email",
                "default_campaign_language",
                "default_footer_text",
                "default_disclaimer",
                "default_email_theme",
                "default_template_width",
                "default_header_logo_enabled",
                "default_footer_enabled",
            )
        }),
        ("Compliance", {
            "fields": (
                "company_legal_name",
                "business_phone",
                "support_email",
                "business_address",
                "city",
                "state",
                "postal_code",
                "unsubscribe_policy",
                "physical_address_required",
                "gdpr_enabled",
                "double_opt_in_enabled",
                "marketing_consent_required",
            )
        }),
        ("Social Links", {
            "fields": (
                "facebook_url",
                "instagram_url",
                "linkedin_url",
                "twitter_url",
                "youtube_url",
                "tiktok_url",
                "whatsapp_number",
            )
        }),
        ("CDP Presets", {
            "fields": (
                "contact_schema_preset",
                "preset_applied",
                "preset_applied_at",
            )
        }),
        ("Plan & Features", {
            "fields": (
                "max_users",
                "max_contacts",
                "max_templates",
                "max_segments",
                "automation_enabled",
                "advanced_segmentation_enabled",
                "webhooks_enabled",
                "ai_features_enabled",
                "custom_branding_enabled",
            )
        }),
        ("Advanced", {
            "fields": (
                "settings",
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "organization",
        "role",
        "status",
        "invited_by",
        "joined_at",
        "last_active_at",
    )
    list_filter = (
        "role",
        "status",
    )
    search_fields = (
        "user__email",
        "organization__name",
        "organization__subdomain",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
