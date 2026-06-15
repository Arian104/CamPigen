import logging

from celery import shared_task
from django.db.models import F
from django.utils import timezone

from .models import WebhookDelivery
from .services import WebhookService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def deliver_webhook(self, delivery_id):
    try:
        delivery = WebhookDelivery.objects.select_related("webhook", "organization").get(id=delivery_id)
    except WebhookDelivery.DoesNotExist:
        logger.error("WebhookDelivery %s not found", delivery_id)
        return {"status": "missing", "delivery_id": str(delivery_id)}

    if delivery.completed_at:
        return {
            "status": "completed",
            "delivery_id": str(delivery.id),
            "success": delivery.success,
        }

    result = WebhookService.send_webhook(
        delivery.webhook,
        delivery.payload,
        delivery.event_type,
    )

    WebhookService.update_delivery(delivery, result)

    if not delivery.success and delivery.next_retry_at and delivery.attempts < delivery.max_attempts:
        delay = max((delivery.next_retry_at - timezone.now()).total_seconds(), 1)
        deliver_webhook.apply_async(args=[str(delivery.id)], countdown=delay)

    return {
        "delivery_id": str(delivery.id),
        "success": delivery.success,
        "attempts": delivery.attempts,
    }


@shared_task
def retry_failed_webhooks(batch_size=100):
    due_deliveries = (
        WebhookDelivery.objects
        .filter(
            success=False,
            completed_at__isnull=True,
            next_retry_at__lte=timezone.now(),
            attempts__lt=F("max_attempts"),
        )
        .order_by("next_retry_at")[:batch_size]
    )

    count = 0

    for delivery in due_deliveries:
        deliver_webhook.delay(str(delivery.id))
        count += 1

    logger.info("Queued %s failed webhooks for retry", count)
    return {"retried_count": count}
