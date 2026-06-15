from django.db import models
from core.models import TimeStampedModel, OrganizationScopedModel

class Automation(OrganizationScopedModel, TimeStampedModel):
    """Marketing automation workflow"""
    TRIGGER_CHOICES = [
        ('form_submitted', 'Form Submitted'),
        ('email_opened', 'Email Opened'),
        ('email_clicked', 'Email Clicked'),
        ('tag_added', 'Tag Added'),
        ('date_based', 'Date Based'),
        ('list_joined', 'List Joined'),
    ]
    
    name = models.CharField(max_length=255)
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    trigger_config = models.JSONField(default=dict)  # e.g., {"campaign_id": 123, "tag_name": "VIP"}
    is_active = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'is_active']),
        ]
    
    def __str__(self):
        return self.name

class AutomationStep(models.Model):
    """Individual step in an automation workflow"""
    STEP_TYPES = [
        ('send_email', 'Send Email'),
        ('wait', 'Wait/Delay'),
        ('add_tag', 'Add Tag'),
        ('remove_tag', 'Remove Tag'),
        ('add_to_list', 'Add to List'),
        ('remove_from_list', 'Remove from List'),
        ('webhook', 'Webhook'),
        ('condition', 'Condition/Split'),
    ]
    
    automation = models.ForeignKey(Automation, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()
    step_type = models.CharField(max_length=50, choices=STEP_TYPES)
    config = models.JSONField(default=dict)  # e.g., {"campaign_id": 456, "delay_minutes": 30}
    delay_minutes = models.IntegerField(default=0)  # For wait steps
    
    class Meta:
        ordering = ['order']
        unique_together = [('automation', 'order')]
    
    def __str__(self):
        return f"{self.automation.name} - Step {self.order}"
