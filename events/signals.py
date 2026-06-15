from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmailEvent
from webhooks.services import WebhookService


EVENT_TO_WEBHOOK_EVENT = {
    "sent": "email.sent",
    "delivered": "email.delivered",
    "opened": "email.opened",
    "clicked": "email.clicked",
    "bounced": "email.bounced",
    "unsubscribed": "contact.unsubscribed",
}


@receiver(post_save, sender=EmailEvent)
def dispatch_webhook_for_email_event(sender, instance, created, **kwargs):
    if not created:
        return

    webhook_event_type = EVENT_TO_WEBHOOK_EVENT.get(instance.event_type)
    if not webhook_event_type:
        return

    organization = getattr(instance.email_job, "organization", None)
    if not organization:
        return

    payload = {
        "event_type": webhook_event_type,
        "email_event_id": str(instance.id),
        "email_job_id": instance.email_job_id,
        "email_job_status": instance.email_job.status,
        "recipient_email": instance.email_job.recipient_email,
        "event_timestamp": instance.timestamp.isoformat(),
        "ip_address": instance.ip_address,
        "user_agent": instance.user_agent,
        "clicked_url": instance.clicked_url,
        "metadata": instance.metadata or {},
    }
    WebhookService.dispatch_event(
        organization=organization,
        event_type=webhook_event_type,
        event_data=payload,
        event_id=instance.id,
    )
