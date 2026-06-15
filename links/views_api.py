from django.db.models import Sum, Count, Max
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import TrackedLink, LinkClick
from .serializers import TrackedLinkSerializer, LinkClickSerializer
from .services import LinkService


def get_active_organization(user):
    return getattr(user, "active_organization", None)


class TrackedLinkViewSet(viewsets.ModelViewSet):
    serializer_class = TrackedLinkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "campaign", "contact", "email_job"]
    search_fields = ["name", "original_url", "tracking_code"]
    ordering_fields = ["last_clicked_at", "click_count", "unique_click_count", "name"]
    ordering = ["-last_clicked_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return TrackedLink.objects.all()

        org = get_active_organization(user)
        if not org:
            return TrackedLink.objects.none()

        return TrackedLink.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = get_active_organization(self.request.user)
        if not org:
            raise ValueError("No active organization selected.")

        serializer.save(
            organization=org,
            tracking_code=LinkService.generate_tracking_code(),
        )

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        link = self.get_object()
        link.is_active = False
        link.save(update_fields=["is_active"])
        return Response({"message": "Tracked link paused."})

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        link = self.get_object()
        link.is_active = True
        link.save(update_fields=["is_active"])
        return Response({"message": "Tracked link resumed."})

    @action(detail=True, methods=["get"])
    def clicks(self, request, pk=None):
        link = self.get_object()
        clicks = link.clicks.select_related("campaign", "contact", "email_job").all()[:100]
        serializer = LinkClickSerializer(clicks, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=["get"])
    def groups(self, request):
        qs = self.get_queryset()

        grouped = (
            qs.values(
                "campaign",
                "campaign__name",
                "original_url",
            )
            .annotate(
                link_count=Count("id"),
                total_clicks=Sum("click_count"),
                unique_clicks=Sum("unique_click_count"),
                last_clicked_at=Max("last_clicked_at"),
            )
            .order_by("-total_clicks", "-last_clicked_at")
        )

        data = []

        for row in grouped:
            data.append({
                "campaign_id": row["campaign"],
                "campaign_name": row["campaign__name"] or "Manual / No Campaign",
                "original_url": row["original_url"],
                "link_count": row["link_count"] or 0,
                "total_clicks": row["total_clicks"] or 0,
                "unique_clicks": row["unique_clicks"] or 0,
                "last_clicked_at": row["last_clicked_at"],
            })

        return Response(data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()

        aggregate = qs.aggregate(
            total_clicks=Sum("click_count"),
            total_unique_clicks=Sum("unique_click_count"),
        )

        return Response({
            "total_links": qs.count(),
            "active_links": qs.filter(is_active=True).count(),
            "inactive_links": qs.filter(is_active=False).count(),
            "expired_links": qs.filter(expires_at__lte=timezone.now()).count(),
            "total_clicks": aggregate["total_clicks"] or 0,
            "total_unique_clicks": aggregate["total_unique_clicks"] or 0,
        })


class LinkClickViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LinkClickSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "tracked_link",
        "campaign",
        "contact",
        "email_job",
        "is_unique",
        "device_type",
        "browser",
    ]
    ordering_fields = ["clicked_at"]
    ordering = ["-clicked_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return LinkClick.objects.all()

        org = get_active_organization(user)
        if not org:
            return LinkClick.objects.none()

        return LinkClick.objects.filter(organization=org)
