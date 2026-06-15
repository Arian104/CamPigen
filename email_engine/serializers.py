from rest_framework import serializers

from .models import EmailJob, SMTPConfig
from .services import SMTPPasswordService

try:
    from .models import SMTPDeliveryAttempt
except ImportError:
    SMTPDeliveryAttempt = None


class EmailJobSerializer(serializers.ModelSerializer):
    contact_email = serializers.EmailField(source="contact.email", read_only=True)
    campaign_name = serializers.CharField(source="campaign.name", read_only=True)
    smtp_name = serializers.SerializerMethodField()

    class Meta:
        model = EmailJob
        fields = [
            "id",
            "campaign",
            "campaign_name",
            "contact",
            "contact_email",
            "organization",
            "email_type",
            "priority",
            "recipient_email",
            "recipient_name",
            "recipient_phone",
            "from_email",
            "from_name",
            "reply_to",
            "subject_snapshot",
            "body_snapshot",
            "html_body",
            "status",
            "scheduled_at",
            "attempts",
            "max_attempts",
            "next_retry_at",
            "error_message",
            "sent_at",
            "use_custom_smtp",
            "custom_smtp_config",
            "smtp_name",
        ]

    def get_smtp_name(self, obj):
        smtp = getattr(obj, "last_smtp_config", None) or getattr(obj, "custom_smtp_config", None)
        return getattr(smtp, "name", "") if smtp else ""


class SMTPConfigSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        trim_whitespace=False,
    )

    organization_name = serializers.CharField(source="organization.name", read_only=True)

    is_in_cooldown = serializers.SerializerMethodField()
    daily_remaining = serializers.SerializerMethodField()
    hourly_remaining = serializers.SerializerMethodField()
    minute_remaining = serializers.SerializerMethodField()


    class Meta:
        model = SMTPConfig
        fields = [
            "id",
            "organization",
            "organization_name",

            "name",
            "smtp_type",
            "host",
            "port",
            "username",
            "password",

            "use_tls",
            "use_ssl",

            "from_email",
            "from_name",
            "reply_to_email",

            "priority",
            "is_active",
            "is_default",

            "daily_limit",
            "hourly_limit",
            "minute_limit",

            "sent_today",
            "sent_this_hour",
            "sent_this_minute",

            "last_reset_at",
            "last_hourly_reset_at",
            "last_minute_reset_at",

            "success_count",
            "failure_count",
            "last_success_at",
            "last_failed_at",
            "last_used_at",

            "health_score",
            "cooldown_until",
            "cooldown_minutes",
            "max_failures_before_cooldown",

            "allowed_email_types",
            "allowed_domains",

            "last_tested_at",
            "last_test_status",
            "last_test_message",

            "is_in_cooldown",
            "daily_remaining",
            "hourly_remaining",
            "minute_remaining",

        ]

        read_only_fields = [
            "id",
            "organization",
            "organization_name",

            "sent_today",
            "sent_this_hour",
            "sent_this_minute",

            "last_reset_at",
            "last_hourly_reset_at",
            "last_minute_reset_at",

            "success_count",
            "failure_count",
            "last_success_at",
            "last_failed_at",
            "last_used_at",

            "health_score",
            "cooldown_until",

            "last_tested_at",
            "last_test_status",
            "last_test_message",

            "is_in_cooldown",
            "daily_remaining",
            "hourly_remaining",
            "minute_remaining",

        ]


    def get_updated_at(self, obj):
        return getattr(obj, None)

    def get_is_in_cooldown(self, obj):
        return bool(getattr(obj, "is_in_cooldown", False))

    def get_daily_remaining(self, obj):
        return getattr(obj, "daily_remaining", 0)

    def get_hourly_remaining(self, obj):
        return getattr(obj, "hourly_remaining", 0)

    def get_minute_remaining(self, obj):
        return getattr(obj, "minute_remaining", 0)

    def validate(self, attrs):
        use_tls = attrs.get("use_tls", getattr(self.instance, "use_tls", False))
        use_ssl = attrs.get("use_ssl", getattr(self.instance, "use_ssl", False))

        if use_tls and use_ssl:
            raise serializers.ValidationError({
                "use_ssl": "Use either TLS or SSL, not both."
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", "")

        if password:
            validated_data["password_encrypted"] = SMTPPasswordService.encrypt(password)

        if "password_encrypted" not in validated_data:
            validated_data["password_encrypted"] = ""

        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", "")

        if password:
            validated_data["password_encrypted"] = SMTPPasswordService.encrypt(password)

        return super().update(instance, validated_data)


if SMTPDeliveryAttempt is not None:
    class SMTPDeliveryAttemptSerializer(serializers.ModelSerializer):
        smtp_name = serializers.CharField(source="smtp_config.name", read_only=True)
        smtp_host = serializers.CharField(source="smtp_config.host", read_only=True)
        job_recipient = serializers.CharField(source="email_job.recipient_email", read_only=True)

        class Meta:
            model = SMTPDeliveryAttempt
            fields = "__all__"
            read_only_fields = ["id"]
else:
    class SMTPDeliveryAttemptSerializer(serializers.Serializer):
        id = serializers.CharField(read_only=True)
        smtp_name = serializers.CharField(read_only=True)
        smtp_host = serializers.CharField(read_only=True)
        job_recipient = serializers.CharField(read_only=True)
