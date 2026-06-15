from django.contrib import admin
from .models import EmailJob, SMTPConfig

@admin.register(EmailJob)
class EmailJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient_email', 'status', 'priority', 'attempts')
    list_filter = ('status', 'priority')
    search_fields = ('recipient_email',)

@admin.register(SMTPConfig)
class SMTPConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'port', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('host',)
