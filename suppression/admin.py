from django.contrib import admin
from .models import SuppressionList

@admin.register(SuppressionList)
class SuppressionListAdmin(admin.ModelAdmin):
    list_display = ('email', 'organization', 'reason')
    list_filter = ('organization', 'reason')
    search_fields = ('email',)
