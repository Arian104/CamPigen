from django.urls import path
from .views_public import redirect_tracked_link

urlpatterns = [
    path("<str:tracking_code>/", redirect_tracked_link, name="redirect-tracked-link"),
]
