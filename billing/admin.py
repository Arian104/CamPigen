from django.contrib import admin
from .models import Plan, Subscription, Invoice

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'price_monthly', 'email_limit_monthly', 'is_active')
    list_filter = ('tier', 'is_active')
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'plan', 'status', 'current_period_end')
    list_filter = ('status', 'plan')
    search_fields = ('organization__name',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'organization', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('invoice_number', 'organization__name')
