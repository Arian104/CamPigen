from django.contrib import admin
from .models import OTP, APIClient

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'code', 'purpose', 'is_used', 'expires_at', 'created_at')
    list_filter = ('purpose', 'is_used', 'created_at')
    search_fields = ('email', 'phone', 'code')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('email', 'phone', 'code', 'purpose')
        }),
        ('Status', {
            'fields': ('is_used', 'expires_at', 'attempts', 'max_attempts')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'organization'),
            'classes': ('collapse',)
        }),
    )

@admin.register(APIClient)
class APIClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'is_active', 'rate_limit_per_minute', 'created_at', 'last_used_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'api_key')
    readonly_fields = ('id', 'api_key', 'created_at', 'last_used_at')
