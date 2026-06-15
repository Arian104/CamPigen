from django.db.models import Count, Sum, Avg
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import EmailJob, SMTPConfig, SMTPDeliveryAttempt
from .serializers import EmailJobSerializer, SMTPConfigSerializer, SMTPDeliveryAttemptSerializer
from .services import EmailService, SMTPPasswordService
from .tasks import process_email_job, process_high_priority_email


def get_active_organization(user):
    return getattr(user, "active_organization", None)


class EmailJobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmailJobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "priority", "campaign", "email_type"]
    ordering_fields = ["created_at", "scheduled_at", "sent_at", "priority"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return EmailJob.objects.all()

        org = get_active_organization(user)
        if not org:
            return EmailJob.objects.none()

        return EmailJob.objects.filter(organization=org)

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        job = self.get_object()

        if job.status not in ["failed", "cancelled"]:
            return Response({"error": "Only failed/cancelled jobs can be retried."}, status=400)

        if job.attempts >= job.max_attempts:
            job.attempts = 0

        job.status = "queued"
        job.next_retry_at = None
        job.error_message = ""
        job.scheduled_at = timezone.now()
        job.save()

        if job.priority >= 8 or job.email_type == "otp":
            process_high_priority_email.delay(job.id)
        else:
            process_email_job.delay(job.id)

        return Response({"message": "Job queued for retry."})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        job = self.get_object()

        if job.status != "queued":
            return Response({"error": "Only queued jobs can be cancelled."}, status=400)

        job.status = "cancelled"
        job.error_message = "Cancelled by user"
        job.save(update_fields=["status", "error_message"])

        return Response({"message": "Job cancelled."})

    @action(detail=True, methods=["get"])
    def attempts(self, request, pk=None):
        job = self.get_object()
        attempts = job.delivery_attempts.select_related("smtp_config").all()
        serializer = SMTPDeliveryAttemptSerializer(attempts, many=True)
        return Response(serializer.data)


class SMTPConfigViewSet(viewsets.ModelViewSet):
    serializer_class = SMTPConfigSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["smtp_type", "is_active", "is_default"]
    ordering_fields = ["priority", "health_score", "sent_today", "last_used_at", "created_at"]
    ordering = ["priority", "-health_score"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return SMTPConfig.objects.all()

        org = get_active_organization(user)
        if not org:
            return SMTPConfig.objects.none()

        return SMTPConfig.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = get_active_organization(self.request.user)
        if not org:
            raise ValueError("No active organization selected.")

        password = serializer.validated_data.get("password_encrypted", "")
        serializer.validated_data["password_encrypted"] = SMTPPasswordService.encrypt(password)

        serializer.save(organization=org)

    def perform_update(self, serializer):
        password = serializer.validated_data.get("password_encrypted")

        if password:
            serializer.validated_data["password_encrypted"] = SMTPPasswordService.encrypt(password)
        else:
            serializer.validated_data.pop("password_encrypted", None)

        serializer.save()

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):
        config = self.get_object()
        recipient_email = request.data.get("recipient_email", "")
        success, message = EmailService.test_smtp_connection(config, recipient_email)

        return Response(
            {
                "success": success,
                "message": message,
            },
            status=200 if success else 400,
        )

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        config = self.get_object()
        config.is_active = False
        config.save(update_fields=["is_active"])
        return Response({"message": "SMTP paused."})

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        config = self.get_object()
        config.is_active = True
        config.cooldown_until = None
        config.save(update_fields=["is_active", "cooldown_until"])
        return Response({"message": "SMTP resumed."})

    @action(detail=True, methods=["post"])
    def reset_counters(self, request, pk=None):
        config = self.get_object()
        config.sent_today = 0
        config.sent_this_hour = 0
        config.sent_this_minute = 0
        config.failure_count = 0
        config.cooldown_until = None
        config.health_score = 100.0
        config.save()
        return Response({"message": "SMTP counters reset."})

    @action(detail=True, methods=["post"])
    def set_default(self, request, pk=None):
        config = self.get_object()

        SMTPConfig.objects.filter(
            organization=config.organization,
            is_default=True,
        ).exclude(id=config.id).update(is_default=False)

        config.is_default = True
        config.save(update_fields=["is_default"])

        return Response({"message": f"{config.name or config.host} is now marked as default."})

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()

        total = qs.count()
        active = qs.filter(is_active=True).count()
        inactive = qs.filter(is_active=False).count()
        cooling_down = qs.filter(cooldown_until__gt=timezone.now()).count()

        aggregate = qs.aggregate(
            total_sent_today=Sum("sent_today"),
            total_sent_hour=Sum("sent_this_hour"),
            avg_health=Avg("health_score"),
            total_failures=Sum("failure_count"),
        )

        return Response({
            "total": total,
            "active": active,
            "inactive": inactive,
            "cooling_down": cooling_down,
            "total_sent_today": aggregate["total_sent_today"] or 0,
            "total_sent_hour": aggregate["total_sent_hour"] or 0,
            "avg_health": round(aggregate["avg_health"] or 0, 2),
            "total_failures": aggregate["total_failures"] or 0,
        })


class SMTPDeliveryAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SMTPDeliveryAttemptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "smtp_config", "email_job"]
    ordering_fields = ["created_at", "started_at", "finished_at", "latency_ms"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return SMTPDeliveryAttempt.objects.all()

        org = get_active_organization(user)
        if not org:
            return SMTPDeliveryAttempt.objects.none()

        return SMTPDeliveryAttempt.objects.filter(organization=org)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_email(request):
    data = request.data
    recipient_email = data.get("recipient_email")
    subject = data.get("subject")
    html_body = data.get("html_body", "")
    body_snapshot = data.get("body_snapshot") or data.get("text_body") or html_body or ""
    email_type = data.get("email_type", "custom")
    priority = int(data.get("priority", 5))

    if not recipient_email:
        return Response({"error": "recipient_email required"}, status=400)

    if not subject or not html_body:
        return Response({"error": "subject and html_body required"}, status=400)

    organization = get_active_organization(request.user)

    if not organization:
        return Response({"error": "No active organization selected."}, status=400)

    job = EmailJob.objects.create(
        recipient_email=recipient_email,
        subject_snapshot=subject,
        body_snapshot=body_snapshot,
        html_body=html_body,
        email_type=email_type,
        priority=priority,
        scheduled_at=timezone.now(),
        max_attempts=3,
        status="queued",
        organization=organization,
        from_email=data.get("from_email", ""),
        from_name=data.get("from_name", ""),
        reply_to=data.get("reply_to", ""),
    )

    if priority >= 8 or email_type == "otp":
        process_high_priority_email.delay(job.id)
    else:
        process_email_job.delay(job.id)

    return Response({
        "message": "Email queued successfully.",
        "job_id": str(job.id),
        "status": "queued",
    }, status=202)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_template_to_contact(request):
    data = request.data
    contact_id = data.get("contact_id")
    template_id = data.get("template_id")
    context = data.get("context", {})

    if not contact_id:
        return Response({"error": "contact_id is required"}, status=400)

    if not template_id:
        return Response({"error": "template_id is required"}, status=400)

    organization = get_active_organization(request.user)

    if not organization:
        return Response({"error": "No active organization selected."}, status=400)

    from contacts.models import Contact
    from campaigns.models import EmailTemplate

    try:
        contact = Contact.objects.get(id=contact_id, organization=organization)
    except Contact.DoesNotExist:
        return Response({"error": "Contact not found"}, status=404)

    try:
        template = EmailTemplate.objects.get(id=template_id, organization=organization)
    except EmailTemplate.DoesNotExist:
        return Response({"error": "Template not found"}, status=404)

    full_context = {
        "first_name": getattr(contact, "first_name", "") or "Arian",
        "last_name": getattr(contact, "last_name", "") or "",
        "email": contact.email,
        "company_name": getattr(contact, "company", "") or organization.display_name,
        "organization_name": organization.name,
        "organization_brand_name": organization.display_name,
        "organization_website": organization.website,
        "support_email": organization.support_email,
        "business_address": organization.business_address,
        "facebook_url": organization.facebook_url or "https://facebook.com",
        "instagram_url": organization.instagram_url or "https://instagram.com",
        "linkedin_url": organization.linkedin_url or "https://linkedin.com",
        "whatsapp_number": organization.whatsapp_number or "https://wa.me/",
        **context,
    }

    rendered = template.render(full_context)

    job = EmailJob.objects.create(
        contact=contact,
        organization=organization,
        recipient_email=contact.email,
        recipient_name=f"{full_context['first_name']} {full_context['last_name']}".strip(),
        subject_snapshot=rendered["subject"],
        body_snapshot=rendered.get("text_content", "") or rendered.get("html_content", ""),
        html_body=rendered["html_content"],
        email_type=getattr(template, "template_type", "custom"),
        priority=5,
        scheduled_at=timezone.now(),
        max_attempts=3,
        status="queued",
    )

    process_email_job.delay(job.id)

    return Response({
        "message": "Email queued successfully.",
        "job_id": str(job.id),
        "contact": contact.email,
        "template": template.name,
        "status": "queued",
    }, status=202)
