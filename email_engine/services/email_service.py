import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.utils import timezone

from .password import SMTPPasswordService
from links.services import LinkRewriteService


class EmailService:
    @staticmethod
    def build_sender(job, smtp_config):
        from_email = job.from_email or smtp_config.from_email or smtp_config.username
        from_name = job.from_name or smtp_config.from_name or ""
        reply_to = job.reply_to or smtp_config.reply_to_email or ""

        return from_email, from_name, reply_to

    @staticmethod
    def send_with_custom_smtp(job, smtp_config):
        if job.html_body and not getattr(job, "links_processed", False):
            job.html_body = LinkRewriteService.rewrite_email_html(job)
            job.links_processed = True
            job.save(update_fields=["html_body", "links_processed"])

        password = SMTPPasswordService.decrypt(smtp_config.password_encrypted)
        from_email, from_name, reply_to = EmailService.build_sender(job, smtp_config)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = job.subject_snapshot
        msg["From"] = f"{from_name} <{from_email}>" if from_name else from_email
        msg["To"] = job.recipient_email

        if reply_to:
            msg["Reply-To"] = reply_to

        plain_text = job.body_snapshot or "This email requires an HTML-compatible email client."
        html_text = job.html_body or job.body_snapshot or ""

        msg.attach(MIMEText(plain_text, "plain"))

        if html_text:
            msg.attach(MIMEText(html_text, "html"))

        try:
            if smtp_config.use_ssl:
                server = smtplib.SMTP_SSL(smtp_config.host, smtp_config.port, timeout=30)
            else:
                server = smtplib.SMTP(smtp_config.host, smtp_config.port, timeout=30)

            with server:
                server.ehlo()

                if smtp_config.use_tls and not smtp_config.use_ssl:
                    server.starttls()
                    server.ehlo()

                server.login(smtp_config.username, password)
                server.sendmail(from_email, [job.recipient_email], msg.as_string())

            return True, "Email sent successfully."

        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def test_smtp_connection(smtp_config, recipient_email: str = ""):
        password = SMTPPasswordService.decrypt(smtp_config.password_encrypted)
        test_to = recipient_email or smtp_config.from_email or smtp_config.username
        from_email = smtp_config.from_email or smtp_config.username

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "SMTP Test Email"
        msg["From"] = from_email
        msg["To"] = test_to
        msg.attach(MIMEText("SMTP test successful.", "plain"))

        try:
            if smtp_config.use_ssl:
                server = smtplib.SMTP_SSL(smtp_config.host, smtp_config.port, timeout=20)
            else:
                server = smtplib.SMTP(smtp_config.host, smtp_config.port, timeout=20)

            with server:
                server.ehlo()

                if smtp_config.use_tls and not smtp_config.use_ssl:
                    server.starttls()
                    server.ehlo()

                server.login(smtp_config.username, password)
                server.sendmail(from_email, [test_to], msg.as_string())

            smtp_config.last_tested_at = timezone.now()
            smtp_config.last_test_status = "success"
            smtp_config.last_test_message = f"Test email sent to {test_to}"
            smtp_config.health_score = min(float(smtp_config.health_score) + 2.0, 100.0)
            smtp_config.save(update_fields=[
                "last_tested_at",
                "last_test_status",
                "last_test_message",
                "health_score",
            ])

            return True, smtp_config.last_test_message

        except Exception as exc:
            smtp_config.last_tested_at = timezone.now()
            smtp_config.last_test_status = "failed"
            smtp_config.last_test_message = str(exc)
            smtp_config.health_score = max(float(smtp_config.health_score) - 5.0, 0.0)
            smtp_config.save(update_fields=[
                "last_tested_at",
                "last_test_status",
                "last_test_message",
                "health_score",
            ])

            return False, str(exc)

    @staticmethod
    def send_campaign_email(campaign, contact, subject, body_html):
        from django.utils import timezone
        from ..models import EmailJob
        from ..tasks import process_email_job

        job = EmailJob.objects.create(
            campaign=campaign,
            contact=contact,
            organization=campaign.organization,
            recipient_email=contact.email,
            recipient_name=f"{contact.first_name} {contact.last_name}".strip(),
            subject_snapshot=subject,
            body_snapshot=body_html,
            html_body=body_html,
            email_type="campaign",
            from_email=getattr(campaign, "from_email", "") or "",
            priority=5,
            scheduled_at=timezone.now(),
            status="queued",
        )

        process_email_job.delay(job.id)
        return True, "Campaign queued"
