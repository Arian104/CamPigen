from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('track/open/<str:token>/', views.track_open, name='track_open'),
    path('track/click/<str:token>/', views.track_click, name='track_click'),
    path('track/unsubscribe/<str:token>/', views.track_unsubscribe, name='track_unsubscribe'),
]
