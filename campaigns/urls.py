from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='list'),
    path('<int:pk>/', views.campaign_detail, name='detail'),
    path('create/', views.campaign_create, name='create'),
    path('<int:pk>/edit/', views.campaign_edit, name='edit'),
    path('<int:pk>/delete/', views.campaign_delete, name='delete'),
    path('<int:pk>/send/', views.campaign_send, name='send'),
    path('<int:pk>/duplicate/', views.campaign_duplicate, name='duplicate'),
    path('templates/', views.template_list, name='templates'),
    path('templates/<int:pk>/', views.template_detail, name='template_detail'),
]
