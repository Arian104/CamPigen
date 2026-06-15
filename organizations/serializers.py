from rest_framework import serializers
from .models import Organization, OrganizationMembership


class OrganizationSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    favicon_url = serializers.SerializerMethodField()
    template_variables = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "subdomain",
            "plan",
            "industry_type",
            "website",
            "country",
            "timezone",
            "is_active",

            "brand_name",
            "logo",
            "logo_url",
            "favicon",
            "favicon_url",
            "primary_color",
            "secondary_color",
            "accent_color",
            "font_family",
            "button_style",

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

            "contact_schema_preset",
            "preset_applied",
            "preset_applied_at",

            "facebook_url",
            "instagram_url",
            "linkedin_url",
            "twitter_url",
            "youtube_url",
            "tiktok_url",
            "whatsapp_number",

            "max_users",
            "max_contacts",
            "max_templates",
            "max_segments",
            "automation_enabled",
            "advanced_segmentation_enabled",
            "webhooks_enabled",
            "ai_features_enabled",
            "custom_branding_enabled",

            "settings",
            "template_variables",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "plan",
            "preset_applied",
            "preset_applied_at",
            "created_at",
            "updated_at",
            "template_variables",
        ]

    def get_logo_url(self, obj):
        request = self.context.get("request")
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return ""

    def get_favicon_url(self, obj):
        request = self.context.get("request")
        if obj.favicon:
            return request.build_absolute_uri(obj.favicon.url) if request else obj.favicon.url
        return ""

    def get_template_variables(self, obj):
        return obj.get_template_variables()


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "name",
            "subdomain",
            "industry_type",
            "website",
            "country",
            "timezone",
        ]


class OrganizationListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    is_current = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "brand_name",
            "subdomain",
            "plan",
            "industry_type",
            "logo_url",
            "role",
            "is_current",
            "is_active",
        ]

    def get_role(self, obj):
        user = self.context["request"].user
        membership = obj.memberships.filter(user=user).first()
        return membership.role if membership else None

    def get_is_current(self, obj):
        user = self.context["request"].user
        return getattr(user, "active_organization_id", None) == obj.id

    def get_logo_url(self, obj):
        request = self.context.get("request")
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return ""


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = OrganizationMembership
        fields = [
            "id",
            "user",
            "email",
            "first_name",
            "last_name",
            "role",
            "status",
            "invited_by",
            "joined_at",
            "last_active_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "email",
            "first_name",
            "last_name",
            "invited_by",
            "joined_at",
            "last_active_at",
            "created_at",
            "updated_at",
        ]


class AddOrganizationMemberSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=["admin", "manager", "marketer", "analyst", "viewer"],
        default="viewer",
    )


class UpdateOrganizationMemberSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=["admin", "manager", "marketer", "analyst", "viewer"],
        required=False,
    )
    status = serializers.ChoiceField(
        choices=["active", "suspended"],
        required=False,
    )
