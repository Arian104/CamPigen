from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import (
    CampaignAnalyticsViewSet,
    DailyAnalyticsViewSet,
    LinkAnalyticsViewSet,
    analytics_overview,
    refresh_analytics,
)

router = DefaultRouter()
router.register(r"campaigns", CampaignAnalyticsViewSet, basename="analytics-campaigns")
router.register(r"daily", DailyAnalyticsViewSet, basename="analytics-daily")
router.register(r"links", LinkAnalyticsViewSet, basename="analytics-links")

urlpatterns = [
    path("overview/", analytics_overview, name="analytics-overview"),
    path("refresh/", refresh_analytics, name="analytics-refresh"),
    path("", include(router.urls)),
]
