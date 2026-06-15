from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import EmailJob, SMTPConfig

@staff_member_required
def job_list(request):
    jobs = EmailJob.objects.select_related('campaign', 'contact').all()
    return render(request, 'email_engine/jobs.html', {'jobs': jobs})

@staff_member_required
def job_detail(request, pk):
    job = get_object_or_404(EmailJob, id=pk)
    return render(request, 'email_engine/job_detail.html', {'job': job})

@staff_member_required
def smtp_config_list(request):
    configs = SMTPConfig.objects.select_related('organization').all()
    return render(request, 'email_engine/smtp_configs.html', {'configs': configs})
