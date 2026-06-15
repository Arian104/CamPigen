from rest_framework import serializers
from .models import (
    OrganizationAnalytics,
    CampaignAnalytics,
    DailyAnalytics,
    LinkAnalytics,
)


class OrganizationAnalyticsSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = OrganizationAnalytics
        fields = "__all__"


class CampaignAnalyticsSerializer(serializers.ModelSerializer):
    campaign_name = serializers.CharField(source="campaign.name", read_only=True)
    campaign_status = serializers.CharField(source="campaign.status", read_only=True)

    class Meta:
        model = CampaignAnalytics
        fields = "__all__"


class DailyAnalyticsSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = DailyAnalytics
        fields = "__all__"


class LinkAnalyticsSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    campaign_name = serializers.CharField(source="campaign.name", read_only=True)

    class Meta:
        model = LinkAnalytics
        fields = "__all__"
