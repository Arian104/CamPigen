from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views_api import TrackedLinkViewSet, LinkClickViewSet

router = DefaultRouter()
router.register(r"links", TrackedLinkViewSet, basename="links")
router.register(r"link-clicks", LinkClickViewSet, basename="link-clicks")

urlpatterns = [
    path("", include(router.urls)),
]
