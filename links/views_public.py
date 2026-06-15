from django.http import HttpResponseGone, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET

from .models import TrackedLink
from .services import LinkService


@require_GET
def redirect_tracked_link(request, tracking_code):
    tracked_link = get_object_or_404(TrackedLink, tracking_code=tracking_code)

    if not tracked_link.is_active:
        return HttpResponseGone("This link is inactive.")

    if tracked_link.is_expired:
        return HttpResponseGone("This link has expired.")

    if not LinkService.is_safe_redirect_url(tracked_link.original_url):
        return HttpResponseBadRequest("Invalid redirect URL.")

    LinkService.record_click(tracked_link, request)

    return redirect(tracked_link.original_url)
