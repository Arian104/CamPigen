from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from organizations.models import Organization, OrganizationMembership

User = get_user_model()


@receiver(post_save, sender=User)
def setup_default_organization(sender, instance, created, **kwargs):
    """
    When a new user is created:
    - Create a default organization
    - Add user as owner
    - Set active organization
    """
    if not created:
        return

    try:
        if instance.active_organization:
            return

        base_subdomain = slugify(instance.username or instance.email.split("@")[0]) or "workspace"
        subdomain = base_subdomain
        counter = 1

        while Organization.objects.filter(subdomain=subdomain).exists():
            subdomain = f"{base_subdomain}-{counter}"
            counter += 1

        org = Organization.objects.create(
            name=f"{instance.username}'s Organization",
            subdomain=subdomain,
            plan="free",
            owner=instance,
        )

        OrganizationMembership.objects.create(
            user=instance,
            organization=org,
            role="owner",
        )

        instance.active_organization = org
        instance.save(update_fields=["active_organization"])

    except Exception as exc:
        print(f"[Signal Error] Failed to setup organization: {exc}")
