from django.urls import path
from . import views_api

app_name = 'otp'

urlpatterns = [
    path('request/', views_api.request_otp, name='request_otp'),
    path('verify/', views_api.verify_otp, name='verify_otp'),
    path('api-clients/', views_api.create_api_client, name='create_api_client'),
    path('rate-limit/<str:identifier>/', views_api.get_rate_limit_status, name='rate_limit'),
]
