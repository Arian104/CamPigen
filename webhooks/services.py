import hashlib
import hmac
import json
import secrets
from datetime import timedelta

import requests
from django.db import connection
from django.db.models import Q
from django.utils import timezone

from .models import Webhook, WebhookDelivery


class WebhookService:
    @staticmethod
    def generate_secret():
        return secrets.token_urlsafe(48)

    @staticmethod
    def json_payload(payload):
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    @classmethod
    def generate_signature(cls, secret, payload):
        if not secret:
            return ""

        message = cls.json_payload(payload)

        return hmac.new(
            secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @classmethod
    def build_headers(cls, webhook, payload, event_type):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "EmailPlatform-Webhook/1.0",
            "X-Webhook-Event": event_type,
            "X-Webhook-ID": str(webhook.id),
            "X-Webhook-Timestamp": timezone.now().isoformat(),
        }

        if webhook.secret_key:
            signature = cls.generate_signature(webhook.secret_key, payload)
            headers["X-Webhook-Signature"] = f"sha256={signature}"

        if webhook.custom_headers:
            for key, value in webhook.custom_headers.items():
                headers[str(key)] = str(value)

        return headers

    @staticmethod
    def get_webhooks_for_event(organization, event_type):
        if not organization:
            return []

        base_qs = Webhook.objects.filter(
            organization=organization,
            is_active=True,
        )

        if connection.vendor == "sqlite":
            return [
                webhook
                for webhook in base_qs
                if event_type in (webhook.events or [])
            ]

        return base_qs.filter(events__contains=[event_type])

    @staticmethod
    def build_payload(event_type, event_data, event_id=None):
        return {
            "event_id": str(event_id) if event_id else None,
            "event_type": event_type,
            "timestamp": timezone.now().isoformat(),
            "data": event_data or {},
            "webhook_version": "1.0",
        }

    @classmethod
    def create_delivery(cls, webhook, event_type, payload, event_id=None):
        return WebhookDelivery.objects.create(
            webhook=webhook,
            organization=webhook.organization,
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            max_attempts=webhook.retry_count,
            next_retry_at=timezone.now(),
        )

    @classmethod
    def send_webhook(cls, webhook, payload, event_type):
        headers = cls.build_headers(webhook, payload, event_type)

        try:
            response = requests.post(
                webhook.url,
                data=cls.json_payload(payload),
                headers=headers,
                timeout=webhook.timeout_seconds or 10,
            )

            return {
                "success": 200 <= response.status_code < 300,
                "status_code": response.status_code,
                "response_body": response.text[:2000],
                "error": "",
                "request_headers": headers,
            }

        except requests.Timeout:
            return {
                "success": False,
                "status_code": None,
                "response_body": "",
                "error": "Request timeout",
                "request_headers": headers,
            }

        except requests.ConnectionError:
            return {
                "success": False,
                "status_code": None,
                "response_body": "",
                "error": "Connection error",
                "request_headers": headers,
            }

        except Exception as exc:
            return {
                "success": False,
                "status_code": None,
                "response_body": "",
                "error": str(exc),
                "request_headers": headers,
            }

    @staticmethod
    def update_delivery(delivery, result):
        delivery.response_status = result.get("status_code")
        delivery.response_body = result.get("response_body", "")
        delivery.request_headers = result.get("request_headers", {})
        delivery.success = bool(result.get("success"))
        delivery.error_message = result.get("error", "")
        delivery.attempts += 1

        webhook = delivery.webhook
        webhook.last_triggered_at = timezone.now()

        if delivery.success:
            delivery.completed_at = timezone.now()
            delivery.next_retry_at = None
            webhook.last_success_at = timezone.now()
        elif delivery.attempts >= delivery.max_attempts:
            delivery.completed_at = timezone.now()
            delivery.next_retry_at = None
            webhook.last_failure_at = timezone.now()
        else:
            delay_seconds = webhook.retry_delay * (2 ** max(delivery.attempts - 1, 0))
            delivery.next_retry_at = timezone.now() + timedelta(
                seconds=min(delay_seconds, 3600)
            )
            webhook.last_failure_at = timezone.now()

        delivery.save()
        webhook.save(update_fields=[
            "last_triggered_at",
            "last_success_at",
            "last_failure_at",
            "updated_at",
        ])

        return delivery

    @classmethod
    def dispatch_event(cls, organization, event_type, event_data=None, event_id=None):
        webhooks = cls.get_webhooks_for_event(organization, event_type)

        if not webhooks:
            return []

        payload = cls.build_payload(event_type, event_data or {}, event_id)
        deliveries = []

        for webhook in webhooks:
            delivery = cls.create_delivery(webhook, event_type, payload, event_id)

            from .tasks import deliver_webhook
            deliver_webhook.delay(str(delivery.id))

            deliveries.append(delivery)

        return deliveries

    @classmethod
    def send_test(cls, webhook):
        payload = cls.build_payload(
            event_type="test",
            event_data={
                "message": "This is a test webhook notification.",
                "webhook_id": str(webhook.id),
                "webhook_name": webhook.name,
                "organization_id": str(webhook.organization_id),
            },
        )

        return cls.send_webhook(webhook, payload, "test")
