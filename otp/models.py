import uuid
from django.db import models
from core.models import TimeStampedModel

class OTP(TimeStampedModel):
    """OTP model for verification codes"""
    PURPOSE_CHOICES = [
        ('login', 'Login Authentication'),
        ('register', 'Account Registration'),
        ('reset_password', 'Password Reset'),
        ('verify_email', 'Email Verification'),
        ('phone_verify', 'Phone Verification'),
        ('transaction', 'Transaction Confirmation'),
        ('custom', 'Custom Purpose'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    code = models.CharField(max_length=10)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES, default='login')
    
    # Expiry and status
    expires_at = models.DateTimeField(db_index=True)
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    
    # Rate limiting
    request_count = models.IntegerField(default=0)
    first_request_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Organization (for multi-tenant)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email', 'code', 'is_used']),
            models.Index(fields=['phone', 'code', 'is_used']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        identifier = self.email or self.phone
        return f"OTP for {identifier} - {self.purpose}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def can_retry(self):
        return self.attempts < self.max_attempts and not self.is_expired()
    
    def increment_attempts(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])
        return self.attempts

class APIClient(models.Model):
    """API clients for external integrations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=64, unique=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, null=True, blank=True)
    allowed_origins = models.JSONField(default=list, blank=True)
    rate_limit_per_minute = models.IntegerField(default=10)
    rate_limit_per_hour = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.api_key[:8]}..."
    
    def can_make_request(self):
        """Check if client is within rate limits"""
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.is_active:
            return False
        
        # Check last minute
        minute_ago = timezone.now() - timedelta(minutes=1)
        minute_requests = OTP.objects.filter(
            created_at__gte=minute_ago,
            request_count__gt=0
        ).count()
        
        if minute_requests >= self.rate_limit_per_minute:
            return False
        
        # Check last hour
        hour_ago = timezone.now() - timedelta(hours=1)
        hour_requests = OTP.objects.filter(
            created_at__gte=hour_ago
        ).count()
        
        if hour_requests >= self.rate_limit_per_hour:
            return False
        
        return True
