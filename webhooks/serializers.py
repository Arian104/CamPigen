from rest_framework import serializers
from .models import Webhook, WebhookDelivery


class WebhookSerializer(serializers.ModelSerializer):
    delivery_count = serializers.IntegerField(read_only=True)
    success_count = serializers.IntegerField(read_only=True)
    failure_count = serializers.IntegerField(read_only=True)
    secret_preview = serializers.SerializerMethodField()
    secret_key = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Webhook
        fields = [
            "id",
            "organization",
            "name",
            "url",
            "events",
            "secret_key",
            "secret_preview",
            "is_active",
            "retry_count",
            "retry_delay",
            "timeout_seconds",
            "custom_headers",
            "created_by",
            "created_at",
            "updated_at",
            "last_triggered_at",
            "last_success_at",
            "last_failure_at",
            "delivery_count",
            "success_count",
            "failure_count",
        ]
        read_only_fields = [
            "id",
            "organization",
            "created_by",
            "created_at",
            "updated_at",
            "last_triggered_at",
            "last_success_at",
            "last_failure_at",
            "delivery_count",
            "success_count",
            "failure_count",
            "secret_preview",
        ]

    def get_secret_preview(self, obj):
        if not obj.secret_key:
            return ""
        return f"{obj.secret_key[:6]}...{obj.secret_key[-4:]}"

    def validate_events(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Events must be a list.")

        valid_events = {item[0] for item in Webhook.EVENT_CHOICES}
        invalid = [event for event in value if event not in valid_events]

        if invalid:
            raise serializers.ValidationError(f"Invalid events: {', '.join(invalid)}")

        return value

    def validate_custom_headers(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Custom headers must be an object.")

        blocked = {"host", "content-length", "connection"}

        for key in value.keys():
            if str(key).lower() in blocked:
                raise serializers.ValidationError(f"Header '{key}' is not allowed.")

        return value


class WebhookDeliverySerializer(serializers.ModelSerializer):
    webhook_name = serializers.CharField(source="webhook.name", read_only=True)
    webhook_url = serializers.CharField(source="webhook.url", read_only=True)

    class Meta:
        model = WebhookDelivery
        fields = [
            "id",
            "organization",
            "webhook",
            "webhook_name",
            "webhook_url",
            "event",
            "event_type",
            "payload",
            "request_headers",
            "response_status",
            "response_body",
            "success",
            "attempts",
            "max_attempts",
            "next_retry_at",
            "error_message",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
