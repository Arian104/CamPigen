from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import hashlib
import hmac
from .services import OTPService
from .models import APIClient

def verify_api_key(request):
    """Verify API key for external clients"""
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None
    
    try:
        client = APIClient.objects.get(api_key=api_key, is_active=True)
        client.last_used_at = timezone.now()
        client.save(update_fields=['last_used_at'])
        return client
    except APIClient.DoesNotExist:
        return None


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def request_otp(request):
    """
    Request an OTP to be sent.
    
    Request body:
    {
        "identifier": "user@example.com or +1234567890",
        "purpose": "login|register|reset_password|verify_email",
        "delivery_method": "email|sms"
    }
    """
    data = request.data
    identifier = data.get('identifier')
    purpose = data.get('purpose', 'login')
    delivery_method = data.get('delivery_method', 'email')
    
    if not identifier:
        return Response(
            {"error": "identifier is required (email or phone)"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get client info
    client = verify_api_key(request)
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    success, result = OTPService.request_otp(
        identifier=identifier,
        purpose=purpose,
        delivery_method=delivery_method,
        expiry_minutes=10,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    if success:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response({"error": result}, status=status.HTTP_429_TOO_MANY_REQUESTS)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verify an OTP code.
    
    Request body:
    {
        "identifier": "user@example.com or +1234567890",
        "code": "123456",
        "purpose": "login"
    }
    """
    data = request.data
    identifier = data.get('identifier')
    code = data.get('code')
    purpose = data.get('purpose', 'login')
    
    if not identifier or not code:
        return Response(
            {"error": "identifier and code are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success, message = OTPService.verify_otp(identifier, code, purpose)
    
    if success:
        return Response({"verified": True, "message": message}, status=status.HTTP_200_OK)
    else:
        return Response({"verified": False, "error": message}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_api_client(request):
    """
    Create a new API client (for internal use).
    
    Request body:
    {
        "name": "My App",
        "organization_id": "uuid"
    }
    """
    data = request.data
    name = data.get('name')
    organization_id = data.get('organization_id')
    
    if not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can create API clients"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    import secrets
    api_key = secrets.token_urlsafe(32)
    
    from organizations.models import Organization
    organization = None
    if organization_id:
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            pass
    
    client = APIClient.objects.create(
        name=name,
        api_key=api_key,
        organization=organization
    )
    
    return Response({
        "id": str(client.id),
        "name": client.name,
        "api_key": api_key,
        "message": "Save this API key - it won't be shown again"
    }, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['GET'])
def get_rate_limit_status(request, identifier):
    """Check rate limit status for an identifier"""
    cache_key = f"otp_rate_limit_{identifier}"
    recent = cache.get(cache_key, [])
    now = timezone.now()
    
    minute_count = sum(1 for t in recent if (now - t).seconds < 60)
    hour_count = len([t for t in recent if (now - t).seconds < 3600])
    
    return Response({
        "identifier": identifier,
        "requests_last_minute": minute_count,
        "requests_last_hour": hour_count,
        "remaining_minute": max(0, 3 - minute_count),
        "remaining_hour": max(0, 10 - hour_count)
    })
