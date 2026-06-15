from django.contrib import admin
from .models import Automation, AutomationStep

class AutomationStepInline(admin.TabularInline):
    model = AutomationStep
    extra = 1

@admin.register(Automation)
class AutomationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'trigger_type', 'is_active')
    list_filter = ('organization', 'trigger_type', 'is_active')
    search_fields = ('name',)
    inlines = [AutomationStepInline]
