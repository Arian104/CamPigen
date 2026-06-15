from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import (
    ContactViewSet,
    ContactFieldDefinitionViewSet,
    ContactListViewSet,
    TagViewSet,
    ContactImportBatchViewSet,
    ContactActivityViewSet,
)

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contacts")
router.register(r"contact-fields", ContactFieldDefinitionViewSet, basename="contact-fields")
router.register(r"contact-lists", ContactListViewSet, basename="contact-lists")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"contact-imports", ContactImportBatchViewSet, basename="contact-imports")
router.register(r"contact-activities", ContactActivityViewSet, basename="contact-activities")

urlpatterns = [
    path("", include(router.urls)),
]
