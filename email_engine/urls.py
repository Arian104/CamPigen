from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import (
    EmailJobViewSet,
    SMTPConfigViewSet,
    SMTPDeliveryAttemptViewSet,
    send_email,
    send_template_to_contact,
)

router = DefaultRouter()
router.register(r"email-jobs", EmailJobViewSet, basename="email-jobs")
router.register(r"smtp-configs", SMTPConfigViewSet, basename="smtp-configs")
router.register(r"smtp-attempts", SMTPDeliveryAttemptViewSet, basename="smtp-attempts")

urlpatterns = [
    path("", include(router.urls)),
    path("send-email/", send_email, name="send-email"),
    path("send-template-to-contact/", send_template_to_contact, name="send-template-to-contact"),
]
