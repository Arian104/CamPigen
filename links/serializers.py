from rest_framework import serializers

from .models import TrackedLink, LinkClick
from .services import LinkService


class TrackedLinkSerializer(serializers.ModelSerializer):
    tracking_url = serializers.SerializerMethodField()
    campaign_name = serializers.CharField(source="campaign.name", read_only=True)
    template_name = serializers.CharField(source="template.name", read_only=True)
    contact_email = serializers.EmailField(source="contact.email", read_only=True)
    contact_name = serializers.SerializerMethodField()
    email_subject = serializers.CharField(source="email_job.subject_snapshot", read_only=True)
    email_recipient = serializers.EmailField(source="email_job.recipient_email", read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    can_redirect = serializers.BooleanField(read_only=True)

    class Meta:
        model = TrackedLink
        fields = [
            "id",
            "organization",

            "campaign",
            "campaign_name",
            "template",
            "template_name",
            "email_job",
            "email_subject",
            "email_recipient",
            "contact",
            "contact_email",
            "contact_name",

            "name",
            "original_url",
            "tracking_code",
            "tracking_url",

            "is_active",
            "is_expired",
            "can_redirect",
            "expires_at",

            "click_count",
            "unique_click_count",
            "last_clicked_at",

            "metadata",
        ]
        read_only_fields = [
            "id",
            "organization",
            "tracking_code",
            "tracking_url",
            "click_count",
            "unique_click_count",
            "last_clicked_at",
            "campaign_name",
            "template_name",
            "contact_email",
            "contact_name",
            "email_subject",
            "email_recipient",
            "is_expired",
            "can_redirect",
        ]

    def get_tracking_url(self, obj):
        return LinkService.build_tracking_url(obj.tracking_code)

    def get_contact_name(self, obj):
        if not obj.contact:
            return ""

        first_name = getattr(obj.contact, "first_name", "") or ""
        last_name = getattr(obj.contact, "last_name", "") or ""
        full_name = f"{first_name} {last_name}".strip()

        return full_name

    def validate_original_url(self, value):
        if not LinkService.is_safe_redirect_url(value):
            raise serializers.ValidationError("Only http and https URLs are allowed.")
        return value


class LinkClickSerializer(serializers.ModelSerializer):
    link_name = serializers.CharField(source="tracked_link.name", read_only=True)
    original_url = serializers.URLField(source="tracked_link.original_url", read_only=True)
    tracking_code = serializers.CharField(source="tracked_link.tracking_code", read_only=True)
    tracking_url = serializers.SerializerMethodField()

    campaign_name = serializers.CharField(source="campaign.name", read_only=True)

    contact_email = serializers.EmailField(source="contact.email", read_only=True)
    contact_name = serializers.SerializerMethodField()

    email_subject = serializers.CharField(source="email_job.subject_snapshot", read_only=True)
    email_recipient = serializers.EmailField(source="email_job.recipient_email", read_only=True)

    class Meta:
        model = LinkClick
        fields = [
            "id",

            "tracked_link",
            "link_name",
            "original_url",
            "tracking_code",
            "tracking_url",

            "organization",

            "campaign",
            "campaign_name",
            "email_job",
            "email_subject",
            "email_recipient",
            "contact",
            "contact_email",
            "contact_name",

            "ip_address",
            "user_agent",
            "referrer",

            "device_type",
            "browser",
            "os",
            "country",

            "is_unique",
            "metadata",
            "clicked_at",
        ]
        read_only_fields = fields

    def get_tracking_url(self, obj):
        if not obj.tracked_link:
            return ""
        return LinkService.build_tracking_url(obj.tracked_link.tracking_code)

    def get_contact_name(self, obj):
        if not obj.contact:
            return ""

        first_name = getattr(obj.contact, "first_name", "") or ""
        last_name = getattr(obj.contact, "last_name", "") or ""

        return f"{first_name} {last_name}".strip()
