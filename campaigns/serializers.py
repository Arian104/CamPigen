from rest_framework import serializers
from .models import EmailTemplate, Campaign


class EmailTemplateSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()

    class Meta:
        model = EmailTemplate
        fields = [
            "id",
            "name",
            "template_type",
            "status",
            "subject",
            "html_content",
            "text_content",
            "builder_schema",
            "variables",
            "preview_data",
            "is_default",
            "usage_count",
            "version",
            "organization",
            "created_by",
            "created_at",
            "updated_at",
            "preview",
        ]

        read_only_fields = [
            "id",
            "organization",
            "created_by",
            "usage_count",
            "version",
            "created_at",
            "updated_at",
            "preview",
        ]

    def get_preview(self, obj):
        sample_context = obj.preview_data or {
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Sample Company",
            "organization_name": "Sample Organization",
            "email": "john@example.com",
        }
        return obj.render(sample_context)


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"

        read_only_fields = [
            "id",
            "organization",
            "total_sent",
            "total_opens",
            "total_clicks",
            "total_bounces",
            "total_unsubscribes",
            "created_at",
            "updated_at",
        ]
