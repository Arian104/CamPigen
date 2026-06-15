import random
import hashlib
import hmac
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.conf import settings
from .models import OTP, APIClient

class OTPService:
    """Enterprise OTP Service with rate limiting and delivery"""
    
    @staticmethod
    def generate_code(length=6):
        """Generate numeric OTP code"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    @staticmethod
    def generate_secure_code(length=8):
        """Generate alphanumeric secure code"""
        import secrets
        import string
        alphabet = string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def get_rate_limit_key(identifier, purpose):
        """Get cache key for rate limiting"""
        return f"otp_rate_limit_{identifier}_{purpose}"
    
    @staticmethod
    def check_rate_limit(identifier, purpose, max_per_minute=3, max_per_hour=10):
        """Check if rate limit is exceeded"""
        cache_key = OTPService.get_rate_limit_key(identifier, purpose)
        
        # Get recent requests from cache
        recent = cache.get(cache_key, [])
        now = timezone.now()
        
        # Clean old entries (older than 1 hour)
        recent = [t for t in recent if (now - t).seconds < 3600]
        
        # Count last minute
        minute_count = sum(1 for t in recent if (now - t).seconds < 60)
        if minute_count >= max_per_minute:
            return False, "Too many requests. Please wait a minute."
        
        # Count last hour
        if len(recent) >= max_per_hour:
            return False, "Rate limit exceeded. Please try again later."
        
        return True, ""
    
    @staticmethod
    def record_request(identifier, purpose):
        """Record a request for rate limiting"""
        cache_key = OTPService.get_rate_limit_key(identifier, purpose)
        recent = cache.get(cache_key, [])
        recent.append(timezone.now())
        cache.set(cache_key, recent, timeout=3600)
    
    @staticmethod
    def create_otp(email=None, phone=None, purpose='login', expiry_minutes=10, 
                   max_attempts=3, ip_address=None, user_agent=None, organization=None):
        """Create a new OTP"""
        identifier = email or phone
        if not identifier:
            raise ValueError("Either email or phone is required")
        
        # Check rate limit
        can_proceed, error_msg = OTPService.check_rate_limit(identifier, purpose)
        if not can_proceed:
            raise Exception(error_msg)
        
        # Generate code
        code = OTPService.generate_code()
        
        # Create OTP record
        otp = OTP.objects.create(
            email=email,
            phone=phone,
            code=code,
            purpose=purpose,
            expires_at=timezone.now() + timedelta(minutes=expiry_minutes),
            max_attempts=max_attempts,
            ip_address=ip_address,
            user_agent=user_agent,
            organization=organization
        )
        
        # Record request for rate limiting
        OTPService.record_request(identifier, purpose)
        
        return otp
    
    @staticmethod
    def verify_otp(identifier, code, purpose='login', mark_used=True):
        """Verify OTP code"""
        from django.db import models
        
        # Find valid OTP
        otp = OTP.objects.filter(
            models.Q(email=identifier) | models.Q(phone=identifier),
            code=code,
            purpose=purpose,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if not otp:
            # Check if any OTP exists for this identifier (to track attempts)
            existing = OTP.objects.filter(
                models.Q(email=identifier) | models.Q(phone=identifier),
                purpose=purpose
            ).first()
            
            if existing:
                existing.increment_attempts()
            
            return False, "Invalid or expired OTP"
        
        if mark_used:
            otp.is_used = True
            otp.save(update_fields=['is_used'])
        
        return True, "OTP verified successfully"
    
    @staticmethod
    def send_otp_via_email(otp, template_id=None):
        """Send OTP via email"""
        from email_engine.services import EmailService
        from email_engine.models import EmailJob
        from django.utils import timezone
        
        if not otp.email:
            return False, "No email address provided"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">Verification Code</h1>
            </div>
            <div style="padding: 30px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
                <p style="font-size: 16px;">Hello,</p>
                <p style="font-size: 16px;">Your verification code is:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <span style="font-size: 36px; font-weight: bold; letter-spacing: 5px; background: white; padding: 15px 30px; border-radius: 10px; border: 1px solid #ddd;">
                        {otp.code}
                    </span>
                </div>
                <p style="font-size: 16px;">This code expires in <strong>{(otp.expires_at - timezone.now()).seconds // 60}</strong> minutes.</p>
                <p style="font-size: 14px; color: #666; margin-top: 30px;">If you didn't request this, please ignore this email.</p>
                <hr style="margin: 20px 0;">
                <p style="font-size: 12px; color: #999; text-align: center;">Email Platform</p>
            </div>
        </body>
        </html>
        """
        
        job = EmailJob.objects.create(
            recipient_email=otp.email,
            subject_snapshot=f"Your {otp.purpose} verification code",
            html_body=html_content,
            email_type='otp',
            priority=10,
            scheduled_at=timezone.now(),
            max_attempts=1,
            status='queued'
        )
        
        from email_engine.tasks import process_high_priority_email
        process_high_priority_email.delay(job.id)
        
        return True, "OTP sent via email"
    
    @staticmethod
    def send_otp_via_sms(otp):
        """Send OTP via SMS (placeholder - integrate with SMS provider)"""
        if not otp.phone:
            return False, "No phone number provided"
        
        # TODO: Integrate with Twilio, AWS SNS, or other SMS provider
        print(f"SMS would be sent to {otp.phone} with code {otp.code}")
        return True, "SMS sent (placeholder)"
    
    @staticmethod
    def send_otp(otp, method='email', template_id=None):
        """Send OTP via specified method"""
        if method == 'email':
            return OTPService.send_otp_via_email(otp, template_id)
        elif method == 'sms':
            return OTPService.send_otp_via_sms(otp)
        else:
            return False, f"Unknown delivery method: {method}"
    
    @staticmethod
    def request_otp(identifier, purpose='login', delivery_method='email', 
                    expiry_minutes=10, ip_address=None, user_agent=None, organization=None):
        """Complete OTP request flow - create and send"""
        # Determine if identifier is email or phone
        email = identifier if '@' in identifier else None
        phone = identifier if not email else None
        
        # Create OTP
        try:
            otp = OTPService.create_otp(
                email=email,
                phone=phone,
                purpose=purpose,
                expiry_minutes=expiry_minutes,
                ip_address=ip_address,
                user_agent=user_agent,
                organization=organization
            )
        except Exception as e:
            return False, str(e)
        
        # Send OTP
        success, message = OTPService.send_otp(otp, delivery_method)
        
        if not success:
            otp.delete()
            return False, message
        
        return True, {
            'message': f'OTP sent successfully via {delivery_method}',
            'expires_in_minutes': expiry_minutes
        }
