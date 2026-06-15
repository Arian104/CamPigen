from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound

from .models import Organization, OrganizationMembership
from .presets import ORGANIZATION_PRESETS

User = get_user_model()


def create_organization(user, validated_data):
    name = validated_data["name"]
    requested_subdomain = validated_data.get("subdomain") or name

    base_subdomain = slugify(requested_subdomain)
    if not base_subdomain:
        base_subdomain = "organization"

    final_subdomain = base_subdomain
    counter = 1

    while Organization.objects.filter(subdomain=final_subdomain).exists():
        final_subdomain = f"{base_subdomain}-{counter}"
        counter += 1

    with transaction.atomic():
        org = Organization.objects.create(
            name=name,
            subdomain=final_subdomain,
            owner=user,
            industry_type=validated_data.get("industry_type", "custom"),
            website=validated_data.get("website", ""),
            country=validated_data.get("country", ""),
            timezone=validated_data.get("timezone", "Asia/Dhaka"),
            brand_name=name,
            default_from_name=name,
        )

        OrganizationMembership.objects.create(
            user=user,
            organization=org,
            role="owner",
            status="active",
            joined_at=timezone.now(),
        )

        user.active_organization = org
        user.save(update_fields=["active_organization"])

    return org


def switch_organization(user, org_id):
    membership = OrganizationMembership.objects.filter(
        user=user,
        organization_id=org_id,
        status="active",
    ).select_related("organization").first()

    if not membership:
        raise PermissionDenied("You do not have access to this organization.")

    user.active_organization = membership.organization
    user.save(update_fields=["active_organization"])

    membership.last_active_at = timezone.now()
    membership.save(update_fields=["last_active_at"])

    return membership.organization


def get_current_organization(user):
    org = getattr(user, "active_organization", None)
    if not org:
        raise ValidationError("No active organization selected.")
    return org


def get_user_membership(user, organization):
    return OrganizationMembership.objects.filter(
        user=user,
        organization=organization,
        status="active",
    ).first()


def ensure_admin_or_owner(user, organization):
    membership = get_user_membership(user, organization)
    if not membership or membership.role not in ["owner", "admin"]:
        raise PermissionDenied("You do not have permission to manage this organization.")
    return membership


def ensure_owner(user, organization):
    membership = get_user_membership(user, organization)
    if not membership or membership.role != "owner":
        raise PermissionDenied("Only organization owner can perform this action.")
    return membership


def add_member(current_user, organization, user_email, role="viewer"):
    actor = ensure_admin_or_owner(current_user, organization)

    if role == "owner" and actor.role != "owner":
        raise PermissionDenied("Only owner can add another owner.")

    try:
        user_to_add = User.objects.get(email=user_email)
    except User.DoesNotExist:
        raise NotFound("User with this email does not exist.")

    if organization.memberships.count() >= organization.max_users:
        raise ValidationError("Organization user limit reached for current plan.")

    membership, created = OrganizationMembership.objects.get_or_create(
        user=user_to_add,
        organization=organization,
        defaults={
            "role": role,
            "status": "active",
            "invited_by": current_user,
            "joined_at": timezone.now(),
        },
    )

    if not created:
        membership.role = role
        membership.status = "active"
        membership.save(update_fields=["role", "status", "updated_at"])

    return membership, created


def update_member(current_user, organization, membership_id, role=None, status=None):
    actor = ensure_admin_or_owner(current_user, organization)

    target = OrganizationMembership.objects.filter(
        id=membership_id,
        organization=organization,
    ).select_related("user").first()

    if not target:
        raise NotFound("Membership not found.")

    if target.role == "owner" and actor.role != "owner":
        raise PermissionDenied("Admin cannot modify owner.")

    if role == "owner" and actor.role != "owner":
        raise PermissionDenied("Only owner can assign owner role.")

    if role:
        target.role = role

    if status:
        target.status = status

    target.save()
    return target


def remove_member(current_user, organization, membership_id):
    actor = ensure_admin_or_owner(current_user, organization)

    target = OrganizationMembership.objects.filter(
        id=membership_id,
        organization=organization,
    ).first()

    if not target:
        raise NotFound("Membership not found.")

    if target.role == "owner" and actor.role != "owner":
        raise PermissionDenied("Admin cannot remove owner.")

    if target.role == "owner":
        owner_count = OrganizationMembership.objects.filter(
            organization=organization,
            role="owner",
            status="active",
        ).count()
        if owner_count <= 1:
            raise ValidationError("Cannot remove the last owner.")

    target.delete()
    return True


def apply_industry_preset(organization, preset_key):
    """
    Safe preset application.
    Creates fields/tags/lists if matching contact models exist.
    """
    preset = ORGANIZATION_PRESETS.get(preset_key)
    if not preset:
        raise ValidationError("Invalid preset.")

    created_summary = {
        "fields": 0,
        "tags": 0,
        "lists": 0,
    }

    try:
        from contacts.models import ContactFieldDefinition, Tag, ContactList
    except Exception:
        organization.contact_schema_preset = preset_key
        organization.preset_applied = True
        organization.preset_applied_at = timezone.now()
        organization.save(update_fields=["contact_schema_preset", "preset_applied", "preset_applied_at"])
        return created_summary

    for field in preset.get("fields", []):
        defaults = {}

        model_fields = [f.name for f in ContactFieldDefinition._meta.fields]

        if "label" in model_fields:
            defaults["label"] = field["name"]
        if "name" in model_fields:
            defaults["name"] = field["name"]
        if "field_type" in model_fields:
            defaults["field_type"] = field["field_type"]
        if "key" in model_fields:
            lookup_key = "key"
            lookup_value = field["key"]
        elif "field_key" in model_fields:
            lookup_key = "field_key"
            lookup_value = field["key"]
            defaults["field_key"] = field["key"]
        else:
            lookup_key = "name"
            lookup_value = field["name"]

        obj, created = ContactFieldDefinition.objects.get_or_create(
            organization=organization,
            **{lookup_key: lookup_value},
            defaults=defaults,
        )
        if created:
            created_summary["fields"] += 1

    for tag_name in preset.get("tags", []):
        model_fields = [f.name for f in Tag._meta.fields]
        lookup = {"organization": organization}

        if "name" in model_fields:
            lookup["name"] = tag_name

        _, created = Tag.objects.get_or_create(**lookup)
        if created:
            created_summary["tags"] += 1

    for list_name in preset.get("lists", []):
        model_fields = [f.name for f in ContactList._meta.fields]
        lookup = {"organization": organization}

        if "name" in model_fields:
            lookup["name"] = list_name

        defaults = {}
        if "list_type" in model_fields:
            defaults["list_type"] = "static"
        if "type" in model_fields:
            defaults["type"] = "static"

        _, created = ContactList.objects.get_or_create(
            **lookup,
            defaults=defaults,
        )
        if created:
            created_summary["lists"] += 1

    organization.industry_type = preset_key
    organization.contact_schema_preset = preset_key
    organization.preset_applied = True
    organization.preset_applied_at = timezone.now()
    organization.save(update_fields=[
        "industry_type",
        "contact_schema_preset",
        "preset_applied",
        "preset_applied_at",
        "updated_at",
    ])

    return created_summary
