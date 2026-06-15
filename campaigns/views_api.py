from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Campaign, EmailTemplate
from .serializers import CampaignSerializer, EmailTemplateSerializer


class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["template_type", "status"]
    search_fields = ["name", "subject"]
    ordering_fields = ["created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return EmailTemplate.objects.all()

        org = getattr(user, "active_organization", None)

        if not org:
            return EmailTemplate.objects.none()

        return EmailTemplate.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = getattr(self.request.user, "active_organization", None)

        serializer.save(
            organization=org,
            created_by=self.request.user,
        )

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        template = self.get_object()

        new_name = request.data.get("name", f"{template.name} (Copy)")

        new_template = EmailTemplate.objects.create(
            organization=template.organization,
            name=new_name,
            template_type=template.template_type,
            subject=template.subject,
            html_content=template.html_content,
            text_content=template.text_content,
            variables=template.variables,
            preview_data=template.preview_data,
            created_by=request.user,
        )

        serializer = EmailTemplateSerializer(new_template)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def preview(self, request, pk=None):
        template = self.get_object()
        context = request.data.get("context", {})
        rendered = template.render(context)

        return Response(rendered)


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["status"]
    search_fields = ["name", "subject"]
    ordering_fields = ["created_at", "scheduled_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Campaign.objects.all()

        org = getattr(user, "active_organization", None)

        if not org:
            return Campaign.objects.none()

        return Campaign.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = getattr(self.request.user, "active_organization", None)

        serializer.save(
            organization=org,
        )

    @action(detail=True, methods=["post"])
    def send_to_contacts(self, request, pk=None):
        campaign = self.get_object()

        from contacts.models import Contact
        from email_engine.services import EmailService

        contacts = Contact.objects.filter(
            organization=campaign.organization,
            lists__in=campaign.target_lists.all(),
        ).distinct()

        sent_count = 0

        for contact in contacts:
            rendered = campaign.get_rendered_content(contact)

            success, msg = EmailService.send_campaign_email(
                campaign,
                contact,
                rendered["subject"],
                rendered["html_content"],
            )

            if success:
                sent_count += 1

        return Response({"message": f"Sent to {sent_count} contacts"})
