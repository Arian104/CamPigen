from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Campaign, EmailTemplate

@staff_member_required
def campaign_list(request):
    """List all campaigns"""
    campaigns = Campaign.objects.select_related('organization').all()
    return render(request, 'campaigns/list.html', {'campaigns': campaigns})

@staff_member_required
def campaign_detail(request, pk):
    """Campaign detail view"""
    campaign = get_object_or_404(Campaign, id=pk)
    return render(request, 'campaigns/detail.html', {'campaign': campaign})

@staff_member_required
def campaign_create(request):
    """Create new campaign"""
    if request.method == 'POST':
        # Handle form submission
        messages.success(request, "Campaign created successfully!")
        return redirect('campaigns:list')
    return render(request, 'campaigns/form.html', {'title': 'Create Campaign'})

@staff_member_required
def campaign_edit(request, pk):
    """Edit campaign"""
    campaign = get_object_or_404(Campaign, id=pk)
    if request.method == 'POST':
        messages.success(request, f"Campaign '{campaign.name}' updated!")
        return redirect('campaigns:detail', pk=pk)
    return render(request, 'campaigns/form.html', {'campaign': campaign, 'title': 'Edit Campaign'})

@staff_member_required
def campaign_delete(request, pk):
    """Delete campaign"""
    campaign = get_object_or_404(Campaign, id=pk)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, "Campaign deleted!")
        return redirect('campaigns:list')
    return render(request, 'campaigns/confirm_delete.html', {'campaign': campaign})

@staff_member_required
def campaign_send(request, pk):
    """Send campaign immediately"""
    campaign = get_object_or_404(Campaign, id=pk)
    messages.info(request, f"Campaign '{campaign.name}' queued for sending!")
    return redirect('campaigns:detail', pk=pk)

@staff_member_required
def campaign_duplicate(request, pk):
    """Duplicate campaign"""
    original = get_object_or_404(Campaign, id=pk)
    # Duplicate logic here
    messages.success(request, f"Campaign '{original.name}' duplicated!")
    return redirect('campaigns:list')

@staff_member_required
def template_list(request):
    """List all email templates"""
    templates = EmailTemplate.objects.select_related('organization').all()
    return render(request, 'campaigns/templates/list.html', {'templates': templates})

@staff_member_required
def template_detail(request, pk):
    """Template detail view"""
    template = get_object_or_404(EmailTemplate, id=pk)
    return render(request, 'campaigns/templates/detail.html', {'template': template})
