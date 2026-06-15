from django.contrib import admin
from .models import EmailTemplate, Campaign

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'template_type', 'status', 'is_default', 'usage_count')
    list_filter = ('organization', 'template_type', 'status', 'is_default')
    search_fields = ('name', 'subject')
    readonly_fields = ('id', 'usage_count', 'version', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('organization', 'name', 'description', 'template_type', 'status')
        }),
        ('Content', {
            'fields': ('subject', 'html_content', 'text_content'),
            'classes': ('wide',)
        }),
        ('Variables & Preview', {
            'fields': ('variables', 'preview_data'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('is_default', 'usage_count', 'version', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'status', 'scheduled_at', 'total_sent')
    list_filter = ('organization', 'status')
    search_fields = ('name', 'subject')
    readonly_fields = ('id', 'total_sent', 'total_opens', 'total_clicks', 'created_at')
    filter_horizontal = ('target_lists',)
