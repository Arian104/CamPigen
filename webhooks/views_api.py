import secrets

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Webhook, WebhookDelivery
from .serializers import WebhookSerializer, WebhookDeliverySerializer
from .services import WebhookService


def get_active_organization(user):
    return getattr(user, "active_organization", None)


class WebhookViewSet(viewsets.ModelViewSet):
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["name", "url"]
    ordering_fields = ["created_at", "last_triggered_at", "last_success_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        qs = Webhook.objects.annotate(
            delivery_count=Count("deliveries"),
            success_count=Count("deliveries", filter=Q(deliveries__success=True)),
            failure_count=Count("deliveries", filter=Q(deliveries__success=False)),
        )

        if user.is_superuser:
            return qs

        org = get_active_organization(user)

        if not org:
            return Webhook.objects.none()

        return qs.filter(organization=org)

    def perform_create(self, serializer):
        org = get_active_organization(self.request.user)

        if not org:
            raise ValidationError({"organization": "No active organization selected."})

        secret_key = serializer.validated_data.get("secret_key") or WebhookService.generate_secret()

        serializer.save(
            organization=org,
            secret_key=secret_key,
            created_by=self.request.user,
        )

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):
        webhook = self.get_object()
        result = WebhookService.send_test(webhook)

        delivery = WebhookService.create_delivery(
            webhook=webhook,
            event_type="test",
            payload=WebhookService.build_payload(
                "test",
                {
                    "message": "This is a test webhook notification.",
                    "webhook_id": str(webhook.id),
                    "webhook_name": webhook.name,
                },
            ),
        )
        WebhookService.update_delivery(delivery, result)

        return Response(
            {
                "success": result.get("success", False),
                "status_code": result.get("status_code"),
                "message": "Test webhook sent." if result.get("success") else "Test webhook failed.",
                "error": result.get("error", ""),
                "delivery_id": str(delivery.id),
            },
            status=status.HTTP_200_OK if result.get("success") else status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        webhook = self.get_object()
        webhook.is_active = False
        webhook.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "Webhook paused."})

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        webhook = self.get_object()
        webhook.is_active = True
        webhook.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "Webhook resumed."})

    @action(detail=True, methods=["post"])
    def regenerate_secret(self, request, pk=None):
        webhook = self.get_object()
        webhook.secret_key = WebhookService.generate_secret()
        webhook.save(update_fields=["secret_key", "updated_at"])
        return Response({
            "message": "Webhook secret regenerated.",
            "secret_preview": f"{webhook.secret_key[:6]}...{webhook.secret_key[-4:]}",
        })

    @action(detail=True, methods=["get"])
    def deliveries(self, request, pk=None):
        webhook = self.get_object()
        deliveries = webhook.deliveries.select_related("webhook").all()[:100]
        serializer = WebhookDeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()

        return Response({
            "total_webhooks": qs.count(),
            "active_webhooks": qs.filter(is_active=True).count(),
            "inactive_webhooks": qs.filter(is_active=False).count(),
            "total_deliveries": WebhookDelivery.objects.filter(webhook__in=qs).count(),
            "successful_deliveries": WebhookDelivery.objects.filter(webhook__in=qs, success=True).count(),
            "failed_deliveries": WebhookDelivery.objects.filter(webhook__in=qs, success=False).count(),
        })


class WebhookDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WebhookDeliverySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["success", "event_type", "webhook"]
    ordering_fields = ["created_at", "completed_at", "attempts"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return WebhookDelivery.objects.select_related("webhook", "organization").all()

        org = get_active_organization(user)

        if not org:
            return WebhookDelivery.objects.none()

        return WebhookDelivery.objects.select_related("webhook", "organization").filter(
            webhook__organization=org
        )

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        delivery = self.get_object()

        if delivery.success:
            return Response({"error": "Delivery already succeeded."}, status=400)

        delivery.completed_at = None
        delivery.next_retry_at = timezone.now()
        delivery.save(update_fields=["completed_at", "next_retry_at", "updated_at"])

        from .tasks import deliver_webhook
        deliver_webhook.delay(str(delivery.id))

        return Response({"message": "Webhook retry queued."})
