from rest_framework.exceptions import PermissionDenied


class OrganizationMixin:
    """
    Standard tenant mixin.
    Everything should use request.user.active_organization.
    """

    def get_organization(self):
        user = self.request.user
        org = getattr(user, "active_organization", None)

        if not org:
            raise PermissionDenied("No active organization selected.")

        return org

    def get_queryset(self):
        qs = super().get_queryset()
        org = self.get_organization()

        if hasattr(qs.model, "organization"):
            return qs.filter(organization=org)

        return qs

    def perform_create(self, serializer):
        if hasattr(serializer.Meta.model, "organization"):
            serializer.save(organization=self.get_organization())
        else:
            serializer.save()
