from django.urls import path, include

urlpatterns = [
    path("organizations/", include("organizations.urls")),
    path("", include("contacts.urls")),
    path("", include("campaigns.urls")),
    path("", include("email_engine.urls")),
    path("", include("webhooks.urls")),
]