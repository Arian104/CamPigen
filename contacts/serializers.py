from django.utils.text import slugify
from rest_framework import serializers

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


class TagSerializer(serializers.ModelSerializer):
    contact_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
            "tag_type",
            "color",
            "description",
            "is_system",
            "is_active",
            "organization",
            "contact_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "organization",
            "is_system",
            "contact_count",
            "created_at",
            "updated_at",
        ]

    def get_contact_count(self, obj):
        return obj.contact_tags.count()

    def validate(self, attrs):
        if not attrs.get("slug") and attrs.get("name"):
            attrs["slug"] = slugify(attrs["name"])
        return attrs


class ContactFieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFieldDefinition
        fields = [
            "id",
            "field_key",
            "label",
            "field_type",
            "options",
            "default_value",
            "is_required",
            "is_filterable",
            "is_visible_in_table",
            "is_importable",
            "help_text",
            "placeholder",
            "order",
            "is_active",
            "organization",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "organization", "created_at", "updated_at"]

    def validate_field_key(self, value):
        return slugify(value).replace("-", "_")


class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    tag_ids = serializers.SerializerMethodField()
    tag_names = serializers.SerializerMethodField()
    list_ids = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "company",
            "job_title",
            "city",
            "country",
            "timezone",
            "language",
            "source",
            "source_detail",
            "lifecycle_stage",
            "lead_score",
            "engagement_score",
            "consent_status",
            "is_unsubscribed",
            "email_verified",
            "email_status",
            "last_emailed_at",
            "last_opened_at",
            "last_clicked_at",
            "last_activity_at",
            "custom_fields",
            "metadata",
            "preferences",
            "tag_ids",
            "tag_names",
            "list_ids",
            "organization",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "tag_ids",
            "tag_names",
            "list_ids",
            "organization",
            "created_at",
            "updated_at",
        ]

    def get_full_name(self, obj):
        return obj.full_name

    def get_tag_ids(self, obj):
        return [str(item.tag_id) for item in obj.contact_tags.select_related("tag")]

    def get_tag_names(self, obj):
        return [item.tag.name for item in obj.contact_tags.select_related("tag")]

    def get_list_ids(self, obj):
        return [str(item.contact_list_id) for item in obj.list_memberships.all()]


class ContactListSerializer(serializers.ModelSerializer):
    contact_count = serializers.SerializerMethodField()

    class Meta:
        model = ContactList
        fields = [
            "id",
            "name",
            "list_type",
            "description",
            "filter_criteria",
            "total_contacts",
            "contact_count",
            "is_active",
            "organization",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "organization",
            "created_by",
            "total_contacts",
            "contact_count",
            "created_at",
            "updated_at",
        ]

    def get_contact_count(self, obj):
        if obj.list_type == "dynamic":
            return obj.total_contacts
        return obj.memberships.count()


class ContactTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactTag
        fields = ["id", "contact", "tag", "added_at", "added_by"]
        read_only_fields = ["id", "added_at", "added_by"]


class ContactListMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListMembership
        fields = ["id", "contact", "contact_list", "added_at", "added_by"]
        read_only_fields = ["id", "added_at", "added_by"]


class ContactImportBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactImportBatch
        fields = "__all__"
        read_only_fields = [
            "id",
            "organization",
            "uploaded_by",
            "created_at",
            "updated_at",
        ]


class ContactActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactActivity
        fields = "__all__"
        read_only_fields = [
            "id",
            "organization",
            "created_at",
            "updated_at",
        ]


class BulkContactImportSerializer(serializers.Serializer):
    contacts = serializers.ListField(child=serializers.DictField())
    list_id = serializers.UUIDField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        default=list,
    )
    overwrite = serializers.BooleanField(default=False)
    source = serializers.CharField(required=False, allow_blank=True, default="csv")


class BulkContactActionSerializer(serializers.Serializer):
    contact_ids = serializers.ListField(child=serializers.UUIDField())
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        default=list,
    )
    list_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        default=list,
    )
