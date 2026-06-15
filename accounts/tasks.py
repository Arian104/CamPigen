import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

from .emails import AccountEmailBuilder

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_email_verification_task(user_id, raw_token):
    user = User.objects.get(id=user_id)

    subject, text, html = AccountEmailBuilder.verification_email(user, raw_token)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        to=[user.email],
    )
    email.attach_alternative(html, "text/html")
    email.send()

    logger.info("Verification email sent to %s", user.email)

    return {"sent": True, "email": user.email}


@shared_task
def send_password_reset_task(user_id, raw_token):
    user = User.objects.get(id=user_id)

    subject, text, html = AccountEmailBuilder.password_reset_email(user, raw_token)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
        to=[user.email],
    )
    email.attach_alternative(html, "text/html")
    email.send()

    logger.info("Password reset email sent to %s", user.email)

    return {"sent": True, "email": user.email}
