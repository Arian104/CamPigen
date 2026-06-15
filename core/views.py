from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    return JsonResponse({
        'message': 'Welcome to Enterprise Email Platform API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_redoc': '/api/redoc/',
            'api_health': '/api/health/',
            'api_v1': '/api/v1/',
            'auth_login': '/api/auth/login/',
            'auth_refresh': '/api/auth/refresh/',
        },
        'documentation': 'Visit /api/docs/ for interactive API documentation'
    })
