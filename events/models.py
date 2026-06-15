from django.db import models
from core.models import TimeStampedModel

class EmailEvent(TimeStampedModel):
    """Track all email events (opens, clicks, bounces, etc.)"""
    EVENT_TYPES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('unsubscribed', 'Unsubscribed'),
        ('complained', 'Complained'),
    ]
    
    email_job = models.ForeignKey('email_engine.EmailJob', on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Additional data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Country, device, browser, etc.
    
    # For click events
    clicked_url = models.URLField(max_length=2000, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email_job', 'event_type']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.email_job.recipient_email} - {self.event_type}"

class LinkClick(models.Model):
    """Track individual link clicks within emails"""
    event = models.OneToOneField(EmailEvent, on_delete=models.CASCADE, related_name='click_detail')
    original_url = models.URLField(max_length=2000)
    redirect_url = models.URLField(max_length=500)
    click_count = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Click on {self.original_url[:50]}"
