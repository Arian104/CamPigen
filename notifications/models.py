from django.db import models
from core.models import TimeStampedModel, OrganizationScopedModel

class NotificationTemplate(OrganizationScopedModel):
    """Templates for in-app and email notifications"""
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('in_app', 'In-App'),
        ('push', 'Push'),
    ]
    
    name = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    subject = models.CharField(max_length=255, blank=True)  # For email
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = [('organization', 'name')]
    
    def __str__(self):
        return self.name

class Notification(TimeStampedModel):
    """Individual notification instance"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('read', 'Read'),
    ]
    
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # For email notifications
    recipient_email = models.EmailField(blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['user', 'read_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification to {self.user or self.recipient_email}"
