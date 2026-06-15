from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import CampaignAnalytics, DailyAnalytics, LinkAnalytics
from .serializers import (
    CampaignAnalyticsSerializer,
    DailyAnalyticsSerializer,
    LinkAnalyticsSerializer,
)
from .services import AnalyticsService


def get_active_organization(user):
    return getattr(user, "active_organization", None)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analytics_overview(request):
    org = get_active_organization(request.user)

    if not org:
        return Response({"error": "No active organization selected."}, status=400)

    return Response(AnalyticsService.build_live_overview(org))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def refresh_analytics(request):
    org = get_active_organization(request.user)

    if not org:
        return Response({"error": "No active organization selected."}, status=400)

    campaign_count = AnalyticsService.refresh_all_campaign_analytics(org)
    link_count = AnalyticsService.refresh_link_analytics(org)
    AnalyticsService.refresh_organization_analytics(org)
    AnalyticsService.refresh_daily_analytics(org)

    return Response({
        "message": "Analytics refreshed.",
        "campaigns_refreshed": campaign_count,
        "link_groups_refreshed": link_count,
    })


class CampaignAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CampaignAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["campaign"]
    ordering_fields = ["total_sent", "total_clicks", "unique_clicks", "last_clicked_at"]
    ordering = ["-total_clicks"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return CampaignAnalytics.objects.select_related("campaign").all()

        org = get_active_organization(user)

        if not org:
            return CampaignAnalytics.objects.none()

        return CampaignAnalytics.objects.select_related("campaign").filter(campaign__organization=org)


class DailyAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DailyAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["date"]
    ordering_fields = ["date", "emails_sent", "clicks", "unique_clicks"]
    ordering = ["-date"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return DailyAnalytics.objects.select_related("organization").all()

        org = get_active_organization(user)

        if not org:
            return DailyAnalytics.objects.none()

        qs = DailyAnalytics.objects.select_related("organization").filter(organization=org)

        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if start:
            parsed = parse_date(start)
            if parsed:
                qs = qs.filter(date__gte=parsed)

        if end:
            parsed = parse_date(end)
            if parsed:
                qs = qs.filter(date__lte=parsed)

        return qs


class LinkAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LinkAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["campaign"]
    ordering_fields = ["generated_links", "total_clicks", "unique_clicks", "last_clicked_at"]
    ordering = ["-total_clicks"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return LinkAnalytics.objects.select_related("organization", "campaign").all()

        org = get_active_organization(user)

        if not org:
            return LinkAnalytics.objects.none()

        return LinkAnalytics.objects.select_related("organization", "campaign").filter(organization=org)
