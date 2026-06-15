from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse

from contacts.views_api import ContactViewSet, ContactListViewSet, TagViewSet
from campaigns.views_api import CampaignViewSet, EmailTemplateViewSet
from email_engine.views_api import EmailJobViewSet, SMTPConfigViewSet, send_email, send_template_to_contact
from otp.views_api import request_otp, verify_otp
from webhooks.views_api import WebhookViewSet, WebhookDeliveryViewSet
from links.views_api import TrackedLinkViewSet, LinkClickViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Email Platform API",
        default_version="v1",
        description="Enterprise Email Marketing Platform API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(r"contact-lists", ContactListViewSet, basename="contact-list")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"campaigns", CampaignViewSet, basename="campaign")
router.register(r"templates", EmailTemplateViewSet, basename="email-template")
router.register(r"email-jobs", EmailJobViewSet, basename="email-job")
router.register(r"smtp-configs", SMTPConfigViewSet, basename="smtp-config")
router.register(r"webhooks", WebhookViewSet, basename="webhook")
router.register(r"webhook-deliveries", WebhookDeliveryViewSet, basename="webhook-delivery")
router.register(r"links", TrackedLinkViewSet, basename="link")
router.register(r"link-clicks", LinkClickViewSet, basename="link-click")

urlpatterns = [
    path("health/", lambda request: JsonResponse({"status": "ok"}), name="health"),

    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path("v1/accounts/", include("accounts.urls")),
    path("v1/organizations/", include("organizations.urls")),
    path("v1/analytics/", include("analytics.urls")),

    path("v1/", include(router.urls)),

    path("send-email/", send_email, name="send_email"),
    path("v1/send-email/", send_email, name="v1_send_email"),
    path("v1/send-template-to-contact/", send_template_to_contact, name="send_template_to_contact"),

    path("otp/request/", request_otp, name="otp_request"),
    path("otp/verify/", verify_otp, name="otp_verify"),
]
