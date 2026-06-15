from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import EmailEvent, LinkClick
from email_engine.models import EmailJob

@csrf_exempt
def track_open(request, token):
    """Track email open (1x1 pixel)"""
    try:
        email_job = EmailJob.objects.get(open_token=token)
        EmailEvent.objects.create(
            email_job=email_job,
            event_type='opened',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except:
        pass
    
    # Return 1x1 transparent GIF
    gif_data = b'GIF89a\x01\x00\x01\x00\x00\xff\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return HttpResponse(gif_data, content_type='image/gif')

@csrf_exempt
def track_click(request, token):
    """Track link click and redirect"""
    try:
        email_job = EmailJob.objects.get(click_token=token)
        original_url = request.GET.get('url', '')
        
        event = EmailEvent.objects.create(
            email_job=email_job,
            event_type='clicked',
            clicked_url=original_url,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        LinkClick.objects.create(
            event=event,
            original_url=original_url,
            redirect_url=original_url
        )
        
        return HttpResponseRedirect(original_url)
    except:
        return HttpResponseRedirect('/')
