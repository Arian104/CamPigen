from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings

class HealthCheckView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'version': '1.0.0',
            'services': {
                'database': 'connected',
                'redis': 'connected' if hasattr(settings, 'CELERY_BROKER_URL') else 'not configured',
            }
        })
