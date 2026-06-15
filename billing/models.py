from django.db import models
from core.models import TimeStampedModel, OrganizationScopedModel

class Plan(models.Model):
    """Subscription plans"""
    PLAN_TIERS = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=20, choices=PLAN_TIERS, unique=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Limits
    email_limit_monthly = models.IntegerField(default=1000)
    contact_limit = models.IntegerField(default=5000)
    campaign_limit = models.IntegerField(default=50)
    api_rate_limit = models.IntegerField(default=60)  # Requests per minute
    
    # Features
    features = models.JSONField(default=list)  # ["api_access", "webhooks", "automations"]
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['price_monthly']
    
    def __str__(self):
        return f"{self.name} - ${self.price_monthly}/mo"

class Subscription(OrganizationScopedModel, TimeStampedModel):
    """Organization subscription"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('trialing', 'Trialing'),
    ]
    
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    
    # Stripe integration (optional)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
        ]
    
    def __str__(self):
        return f"{self.organization.name} - {self.plan.name}"

class Invoice(TimeStampedModel):
    """Billing invoices"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='invoices')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    invoice_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Stripe integration
    stripe_invoice_id = models.CharField(max_length=100, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.amount} {self.currency}"
