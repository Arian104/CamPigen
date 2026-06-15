from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public tracked link redirect
    path('r/', include('links.public_urls')),

    # API routes
    path('api/', include('core.api_urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/campaigns/', include('campaigns.urls')),
    path('api/email-engine/', include('email_engine.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
