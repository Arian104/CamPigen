from django.urls import path
from .views_api import (
    OrganizationListCreateView,
    OrganizationSwitchView,
    CurrentOrganizationView,
    OrganizationTemplateVariablesView,
    OrganizationMembersView,
    OrganizationMemberDetailView,
    OrganizationPresetListView,
    OrganizationApplyPresetView,
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="organization-list-create"),
    path("switch/", OrganizationSwitchView.as_view(), name="organization-switch"),

    path("current/", CurrentOrganizationView.as_view(), name="organization-current"),
    path("current/template-variables/", OrganizationTemplateVariablesView.as_view(), name="organization-template-variables"),

    path("current/members/", OrganizationMembersView.as_view(), name="organization-members"),
    path("current/members/<uuid:membership_id>/", OrganizationMemberDetailView.as_view(), name="organization-member-detail"),

    path("presets/", OrganizationPresetListView.as_view(), name="organization-presets"),
    path("apply-preset/", OrganizationApplyPresetView.as_view(), name="organization-apply-preset"),
]
