from django.contrib import admin
from .models import NotificationTemplate, Notification

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'notification_type', 'is_active')
    list_filter = ('organization', 'notification_type', 'is_active')
    search_fields = ('name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'recipient_email', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'message')
