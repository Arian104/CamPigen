from django.db import models
from core.models import TimeStampedModel, OrganizationScopedModel

class SuppressionList(TimeStampedModel):
    """Global suppression list for bounces, complaints, and unsubscribes"""
    REASON_CHOICES = [
        ('bounce', 'Hard Bounce'),
        ('complaint', 'Spam Complaint'),
        ('unsubscribe', 'Manual Unsubscribe'),
        ('manual', 'Manual Addition'),
    ]
    
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='suppressions')
    email = models.EmailField(db_index=True)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    source = models.CharField(max_length=100, blank=True)  # Which campaign/job caused this
    
    class Meta:
        unique_together = [('organization', 'email')]
        indexes = [
            models.Index(fields=['organization', 'email']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.reason}"
