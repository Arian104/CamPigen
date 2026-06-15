from django.db import models
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from organizations.models import OrganizationMembership
from .models import (
    Contact,
    ContactFieldDefinition,
    Tag,
    ContactTag,
    ContactList,
    ContactListMembership,
    ContactImportBatch,
    ContactActivity,
)
from .serializers import (
    ContactSerializer,
    ContactFieldDefinitionSerializer,
    TagSerializer,
    ContactListSerializer,
    ContactImportBatchSerializer,
    ContactActivitySerializer,
    BulkContactImportSerializer,
    BulkContactActionSerializer,
)


def get_active_organization(user):
    if user.is_superuser:
        return getattr(user, "active_organization", None) or getattr(user, "organization", None)

    org = getattr(user, "active_organization", None) or getattr(user, "organization", None)

    if org:
        is_member = OrganizationMembership.objects.filter(
            user=user,
            organization=org,
        ).exists()

        if is_member:
            return org

    membership = (
        OrganizationMembership.objects
        .filter(user=user)
        .select_related("organization")
        .first()
    )

    return membership.organization if membership else None


class OrganizationScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_organization(self):
        return get_active_organization(self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset.all()

        org = self.get_organization()

        if not org:
            return self.queryset.none()

        return self.queryset.filter(organization=org)

    def perform_create(self, serializer):
        serializer.save(organization=self.get_organization())


class ContactFieldDefinitionViewSet(OrganizationScopedViewSet):
    queryset = ContactFieldDefinition.objects.all()
    serializer_class = ContactFieldDefinitionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["field_type", "is_active", "is_filterable", "is_visible_in_table"]
    search_fields = ["field_key", "label"]
    ordering_fields = ["order", "label", "created_at"]
    ordering = ["order", "label"]


class TagViewSet(OrganizationScopedViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["tag_type", "is_active"]
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["name", "tag_type", "created_at"]
    ordering = ["tag_type", "name"]


class ContactListViewSet(OrganizationScopedViewSet):
    queryset = ContactList.objects.all()
    serializer_class = ContactListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["list_type", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name", "total_contacts"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(
            organization=self.get_organization(),
            created_by=self.request.user,
        )

    @action(detail=True, methods=["get"])
    def contacts(self, request, pk=None):
        contact_list = self.get_object()

        if contact_list.list_type == "dynamic":
            contacts = apply_contact_filters(
                Contact.objects.filter(organization=contact_list.organization),
                contact_list.filter_criteria,
            )
        else:
            contact_ids = contact_list.memberships.values_list("contact_id", flat=True)
            contacts = Contact.objects.filter(id__in=contact_ids)

        page = self.paginate_queryset(contacts)

        if page is not None:
            serializer = ContactSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def refresh_count(self, request, pk=None):
        contact_list = self.get_object()

        if contact_list.list_type == "dynamic":
            total = apply_contact_filters(
                Contact.objects.filter(organization=contact_list.organization),
                contact_list.filter_criteria,
            ).count()
        else:
            total = contact_list.memberships.count()

        contact_list.total_contacts = total
        contact_list.save(update_fields=["total_contacts", "updated_at"])

        return Response({"total_contacts": total})


class ContactViewSet(OrganizationScopedViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "lifecycle_stage",
        "consent_status",
        "is_unsubscribed",
        "country",
        "source",
        "email_verified",
    ]
    search_fields = [
        "email",
        "first_name",
        "last_name",
        "phone",
        "company",
        "city",
        "country",
        "source",
    ]
    ordering_fields = [
        "created_at",
        "email",
        "first_name",
        "lead_score",
        "engagement_score",
        "last_emailed_at",
        "last_opened_at",
        "last_clicked_at",
    ]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        tag_ids = self.request.query_params.getlist("tag")
        list_ids = self.request.query_params.getlist("list")
        min_score = self.request.query_params.get("min_score")
        max_score = self.request.query_params.get("max_score")
        custom_key = self.request.query_params.get("custom_key")
        custom_value = self.request.query_params.get("custom_value")

        if tag_ids:
            queryset = queryset.filter(contact_tags__tag_id__in=tag_ids).distinct()

        if list_ids:
            queryset = queryset.filter(list_memberships__contact_list_id__in=list_ids).distinct()

        if min_score:
            queryset = queryset.filter(lead_score__gte=min_score)

        if max_score:
            queryset = queryset.filter(lead_score__lte=max_score)

        if custom_key and custom_value:
            queryset = queryset.filter(**{f"custom_fields__{custom_key}": custom_value})

        return queryset

    def perform_create(self, serializer):
        contact = serializer.save(organization=self.get_organization())

        ContactActivity.objects.create(
            organization=contact.organization,
            contact=contact,
            activity_type="created",
            title="Contact created",
        )

    @action(detail=True, methods=["post"])
    def add_tags(self, request, pk=None):
        contact = self.get_object()
        tag_ids = request.data.get("tag_ids", [])

        added = 0

        for tag_id in tag_ids:
            tag = Tag.objects.filter(id=tag_id, organization=contact.organization).first()
            if not tag:
                continue

            _, created = ContactTag.objects.get_or_create(
                contact=contact,
                tag=tag,
                defaults={"added_by": request.user},
            )

            if created:
                added += 1

        return Response({"added": added})

    @action(detail=True, methods=["post"])
    def remove_tags(self, request, pk=None):
        contact = self.get_object()
        tag_ids = request.data.get("tag_ids", [])

        deleted, _ = ContactTag.objects.filter(
            contact=contact,
            tag_id__in=tag_ids,
        ).delete()

        return Response({"removed": deleted})

    @action(detail=True, methods=["post"])
    def add_to_lists(self, request, pk=None):
        contact = self.get_object()
        list_ids = request.data.get("list_ids", [])

        added = 0

        for list_id in list_ids:
            contact_list = ContactList.objects.filter(
                id=list_id,
                organization=contact.organization,
            ).first()

            if not contact_list:
                continue

            _, created = ContactListMembership.objects.get_or_create(
                contact=contact,
                contact_list=contact_list,
                defaults={"added_by": request.user},
            )

            if created:
                added += 1

        return Response({"added": added})

    @action(detail=False, methods=["post"])
    def bulk_import(self, request):
        serializer = BulkContactImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        org = self.get_organization()
        contacts_data = serializer.validated_data["contacts"]
        overwrite = serializer.validated_data["overwrite"]
        source = serializer.validated_data.get("source", "csv")
        list_id = serializer.validated_data.get("list_id")
        tag_ids = serializer.validated_data.get("tag_ids", [])

        batch = ContactImportBatch.objects.create(
            organization=org,
            uploaded_by=request.user,
            source=source,
            total_rows=len(contacts_data),
            status="processing",
        )

        contact_list = None
        if list_id:
            contact_list = ContactList.objects.filter(id=list_id, organization=org).first()

        tags = Tag.objects.filter(id__in=tag_ids, organization=org)

        success = 0
        failed = 0
        errors = []

        for index, row in enumerate(contacts_data, start=1):
            email = row.get("email")

            if not email:
                failed += 1
                errors.append({"row": index, "error": "Missing email"})
                continue

            defaults = {
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "phone": row.get("phone", ""),
                "company": row.get("company", ""),
                "job_title": row.get("job_title", ""),
                "city": row.get("city", ""),
                "country": row.get("country", ""),
                "source": row.get("source", source),
                "custom_fields": row.get("custom_fields", {}),
                "metadata": row.get("metadata", {}),
            }

            try:
                contact, created = Contact.objects.get_or_create(
                    organization=org,
                    email=email,
                    defaults=defaults,
                )

                if not created and overwrite:
                    for key, value in defaults.items():
                        setattr(contact, key, value)
                    contact.save()

                if contact_list:
                    ContactListMembership.objects.get_or_create(
                        contact=contact,
                        contact_list=contact_list,
                        defaults={"added_by": request.user},
                    )

                for tag in tags:
                    ContactTag.objects.get_or_create(
                        contact=contact,
                        tag=tag,
                        defaults={"added_by": request.user},
                    )

                success += 1

            except Exception as exc:
                failed += 1
                errors.append({"row": index, "email": email, "error": str(exc)})

        batch.successful_rows = success
        batch.failed_rows = failed
        batch.error_report = errors
        batch.status = "completed" if failed == 0 else "partially_completed"
        batch.save()

        return Response(
            {
                "batch_id": str(batch.id),
                "success": success,
                "failed": failed,
                "errors": errors[:20],
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def bulk_apply(self, request):
        serializer = BulkContactActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        org = self.get_organization()
        contact_ids = serializer.validated_data["contact_ids"]
        tag_ids = serializer.validated_data.get("tag_ids", [])
        list_ids = serializer.validated_data.get("list_ids", [])

        contacts = Contact.objects.filter(id__in=contact_ids, organization=org)
        tags = Tag.objects.filter(id__in=tag_ids, organization=org)
        lists = ContactList.objects.filter(id__in=list_ids, organization=org)

        tag_count = 0
        list_count = 0

        for contact in contacts:
            for tag in tags:
                _, created = ContactTag.objects.get_or_create(
                    contact=contact,
                    tag=tag,
                    defaults={"added_by": request.user},
                )
                if created:
                    tag_count += 1

            for contact_list in lists:
                _, created = ContactListMembership.objects.get_or_create(
                    contact=contact,
                    contact_list=contact_list,
                    defaults={"added_by": request.user},
                )
                if created:
                    list_count += 1

        return Response(
            {
                "contacts": contacts.count(),
                "tags_added": tag_count,
                "lists_added": list_count,
            }
        )

    @action(detail=False, methods=["post"])
    def preview_segment(self, request):
        org = self.get_organization()
        criteria = request.data.get("filter_criteria", {})

        queryset = apply_contact_filters(
            Contact.objects.filter(organization=org),
            criteria,
        )

        serializer = ContactSerializer(queryset[:50], many=True)

        return Response(
            {
                "count": queryset.count(),
                "preview": serializer.data,
            }
        )


class ContactImportBatchViewSet(OrganizationScopedViewSet):
    queryset = ContactImportBatch.objects.all()
    serializer_class = ContactImportBatchSerializer
    http_method_names = ["get", "head", "options"]


class ContactActivityViewSet(OrganizationScopedViewSet):
    queryset = ContactActivity.objects.all()
    serializer_class = ContactActivitySerializer
    http_method_names = ["get", "head", "options"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["contact", "activity_type", "campaign"]
    ordering = ["-created_at"]


def apply_contact_filters(queryset, criteria):
    if not criteria:
        return queryset

    include_tags = criteria.get("include_tags", [])
    exclude_tags = criteria.get("exclude_tags", [])
    lifecycle_stages = criteria.get("lifecycle_stages", [])
    countries = criteria.get("countries", [])
    sources = criteria.get("sources", [])
    custom_fields = criteria.get("custom_fields", {})
    min_lead_score = criteria.get("min_lead_score")
    min_engagement_score = criteria.get("min_engagement_score")
    exclude_unsubscribed = criteria.get("exclude_unsubscribed", True)

    if include_tags:
        queryset = queryset.filter(contact_tags__tag_id__in=include_tags).distinct()

    if exclude_tags:
        queryset = queryset.exclude(contact_tags__tag_id__in=exclude_tags)

    if lifecycle_stages:
        queryset = queryset.filter(lifecycle_stage__in=lifecycle_stages)

    if countries:
        queryset = queryset.filter(country__in=countries)

    if sources:
        queryset = queryset.filter(source__in=sources)

    if custom_fields:
        for key, value in custom_fields.items():
            if value not in [None, ""]:
                queryset = queryset.filter(**{f"custom_fields__{key}": value})

    if min_lead_score is not None:
        queryset = queryset.filter(lead_score__gte=min_lead_score)

    if min_engagement_score is not None:
        queryset = queryset.filter(engagement_score__gte=min_engagement_score)

    if exclude_unsubscribed:
        queryset = queryset.filter(is_unsubscribed=False).exclude(
            consent_status__in=["unsubscribed", "bounced", "complained", "suppressed"]
        )

    return queryset
