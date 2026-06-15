from rest_framework.permissions import BasePermission
from .models import OrganizationMembership


ROLE_LEVELS = {
    "viewer": 10,
    "analyst": 20,
    "marketer": 30,
    "manager": 40,
    "admin": 80,
    "owner": 100,
}


def get_active_membership(user):
    org = getattr(user, "active_organization", None)
    if not user or not user.is_authenticated or not org:
        return None

    return OrganizationMembership.objects.filter(
        user=user,
        organization=org,
        status="active",
    ).first()


class IsOrganizationMember(BasePermission):
    def has_permission(self, request, view):
        return get_active_membership(request.user) is not None


class RolePermission(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        membership = get_active_membership(request.user)
        if not membership:
            return False
        return membership.role in self.allowed_roles


class IsOwner(RolePermission):
    allowed_roles = ["owner"]


class IsAdmin(RolePermission):
    allowed_roles = ["owner", "admin"]


class IsManager(RolePermission):
    allowed_roles = ["owner", "admin", "manager"]


class IsMarketer(RolePermission):
    allowed_roles = ["owner", "admin", "manager", "marketer"]


class IsAnalyst(RolePermission):
    allowed_roles = ["owner", "admin", "manager", "analyst"]


class IsViewer(RolePermission):
    allowed_roles = ["owner", "admin", "manager", "marketer", "analyst", "viewer"]
