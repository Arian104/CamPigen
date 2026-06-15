from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Organization, OrganizationMembership
from .serializers import (
    OrganizationSerializer,
    OrganizationCreateSerializer,
    OrganizationListSerializer,
    OrganizationMembershipSerializer,
    AddOrganizationMemberSerializer,
    UpdateOrganizationMemberSerializer,
)
from .services import (
    create_organization,
    switch_organization,
    get_current_organization,
    add_member,
    update_member,
    remove_member,
    apply_industry_preset,
)
from .presets import ORGANIZATION_PRESETS
from .permissions import IsOrganizationMember, IsAdmin


class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organizations = Organization.objects.filter(
            memberships__user=request.user,
            memberships__status="active",
        ).distinct()
        serializer = OrganizationListSerializer(
            organizations,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        org = create_organization(request.user, serializer.validated_data)

        return Response(
            OrganizationSerializer(org, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class OrganizationSwitchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        org_id = request.data.get("organization_id")
        if not org_id:
            return Response({"error": "organization_id is required"}, status=400)

        org = switch_organization(request.user, org_id)
        return Response({
            "message": f"Switched to {org.name}",
            "organization": OrganizationSerializer(org, context={"request": request}).data,
        })


class CurrentOrganizationView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        org = get_current_organization(request.user)
        return Response(OrganizationSerializer(org, context={"request": request}).data)

    def patch(self, request):
        org = get_current_organization(request.user)

        membership = OrganizationMembership.objects.filter(
            user=request.user,
            organization=org,
            status="active",
        ).first()

        if not membership or membership.role not in ["owner", "admin"]:
            return Response({"error": "Only owner/admin can update organization."}, status=403)

        serializer = OrganizationSerializer(
            org,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class OrganizationTemplateVariablesView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        org = get_current_organization(request.user)
        return Response(org.get_template_variables())


class OrganizationMembersView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        org = get_current_organization(request.user)
        members = OrganizationMembership.objects.filter(
            organization=org,
        ).select_related("user", "invited_by").order_by("role", "created_at")

        serializer = OrganizationMembershipSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request):
        org = get_current_organization(request.user)

        serializer = AddOrganizationMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        membership, created = add_member(
            current_user=request.user,
            organization=org,
            user_email=serializer.validated_data["user_email"],
            role=serializer.validated_data["role"],
        )

        return Response(
            {
                "message": "Member added successfully" if created else "Member updated successfully",
                "created": created,
                "member": OrganizationMembershipSerializer(membership).data,
            },
            status=status.HTTP_201_CREATED,
        )


class OrganizationMemberDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def patch(self, request, membership_id):
        org = get_current_organization(request.user)

        serializer = UpdateOrganizationMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        membership = update_member(
            current_user=request.user,
            organization=org,
            membership_id=membership_id,
            role=serializer.validated_data.get("role"),
            status=serializer.validated_data.get("status"),
        )

        return Response(OrganizationMembershipSerializer(membership).data)

    def delete(self, request, membership_id):
        org = get_current_organization(request.user)

        remove_member(
            current_user=request.user,
            organization=org,
            membership_id=membership_id,
        )

        return Response({"message": "Member removed successfully."}, status=200)


class OrganizationPresetListView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response({
            "presets": [
                {
                    "key": key,
                    "label": key.replace("_", " ").title(),
                    "fields": value.get("fields", []),
                    "tags": value.get("tags", []),
                    "lists": value.get("lists", []),
                }
                for key, value in ORGANIZATION_PRESETS.items()
            ]
        })


class OrganizationApplyPresetView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        org = get_current_organization(request.user)
        preset_key = request.data.get("preset_key")

        if not preset_key:
            return Response({"error": "preset_key is required"}, status=400)

        summary = apply_industry_preset(org, preset_key)

        return Response({
            "message": "Preset applied successfully.",
            "preset_key": preset_key,
            "created": summary,
            "organization": OrganizationSerializer(org, context={"request": request}).data,
        })
