from django.contrib import admin
from .models import EmailEvent, LinkClick

@admin.register(EmailEvent)
class EmailEventAdmin(admin.ModelAdmin):
    list_display = ('email_job', 'event_type', 'timestamp', 'ip_address')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('email_job__recipient_email', 'ip_address')
    readonly_fields = ('timestamp',)
    
@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = ('event', 'original_url', 'click_count')
    search_fields = ('original_url',)
