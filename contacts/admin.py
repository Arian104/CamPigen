from django.contrib import admin

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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "organization",
        "company",
        "country",
        "lifecycle_stage",
        "lead_score",
        "engagement_score",
        "consent_status",
        "is_unsubscribed",
    )
    list_filter = (
        "organization",
        "lifecycle_stage",
        "consent_status",
        "is_unsubscribed",
        "country",
        "source",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "company",
        "city",
        "country",
    )
    readonly_fields = (
        "id",
        "unsubscribe_token",
        "created_at",
        "updated_at",
        "last_emailed_at",
        "last_opened_at",
        "last_clicked_at",
        "last_activity_at",
    )


@admin.register(ContactFieldDefinition)
class ContactFieldDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "field_key",
        "field_type",
        "organization",
        "is_filterable",
        "is_visible_in_table",
        "is_active",
        "order",
    )
    list_filter = (
        "organization",
        "field_type",
        "is_filterable",
        "is_visible_in_table",
        "is_active",
    )
    search_fields = ("label", "field_key")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "tag_type",
        "color",
        "organization",
        "is_system",
        "is_active",
    )
    list_filter = ("organization", "tag_type", "is_system", "is_active")
    search_fields = ("name", "slug", "description")


@admin.register(ContactTag)
class ContactTagAdmin(admin.ModelAdmin):
    list_display = ("contact", "tag", "added_at", "added_by")
    list_filter = ("tag__tag_type", "tag__organization")
    search_fields = ("contact__email", "tag__name")


@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "list_type",
        "organization",
        "total_contacts",
        "is_active",
        "created_by",
    )
    list_filter = ("organization", "list_type", "is_active")
    search_fields = ("name", "description")


@admin.register(ContactListMembership)
class ContactListMembershipAdmin(admin.ModelAdmin):
    list_display = ("contact", "contact_list", "added_at", "added_by")
    list_filter = ("contact_list__organization",)
    search_fields = ("contact__email", "contact_list__name")


@admin.register(ContactImportBatch)
class ContactImportBatchAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "organization",
        "source",
        "status",
        "total_rows",
        "successful_rows",
        "failed_rows",
        "uploaded_by",
        "created_at",
    )
    list_filter = ("organization", "status", "source")
    search_fields = ("file_name", "source")


@admin.register(ContactActivity)
class ContactActivityAdmin(admin.ModelAdmin):
    list_display = (
        "contact",
        "activity_type",
        "title",
        "organization",
        "campaign",
        "created_at",
    )
    list_filter = ("organization", "activity_type")
    search_fields = ("contact__email", "title", "description")
