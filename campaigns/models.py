import uuid
import re

from django.db import models
from django.template import Template, Context

from core.models import TimeStampedModel


class EmailTemplate(TimeStampedModel):
    TEMPLATE_TYPES = [
        ('marketing', 'Marketing Campaign'),
        ('transactional', 'Transactional Email'),
        ('otp', 'OTP / Verification'),
        ('welcome', 'Welcome Email'),
        ('newsletter', 'Newsletter'),
        ('custom', 'Custom Template'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='email_templates'
    )

    # =========================================================
    # BASIC INFO
    # =========================================================

    name = models.CharField(max_length=255)

    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        default='marketing'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # =========================================================
    # TEMPLATE CONTENT
    # =========================================================

    subject = models.CharField(max_length=255)

    # Final compiled email HTML
    html_content = models.TextField()

    # Optional text version
    text_content = models.TextField(blank=True)

    # =========================================================
    # VISUAL BUILDER
    # =========================================================

    builder_schema = models.JSONField(
        default=dict,
        blank=True,
        help_text="Visual drag-and-drop email builder schema"
    )

    # =========================================================
    # VARIABLES
    # =========================================================

    variables = models.JSONField(
        default=list,
        blank=True,
        help_text='Example: ["first_name", "company_name", "reset_link"]'
    )

    # =========================================================
    # PREVIEW
    # =========================================================

    preview_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Sample data used for live preview rendering'
    )

    # =========================================================
    # METADATA
    # =========================================================

    is_default = models.BooleanField(default=False)

    usage_count = models.IntegerField(default=0)

    version = models.IntegerField(default=1)

    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

        unique_together = [['organization', 'name']]

        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['organization', 'template_type']),
            models.Index(fields=['is_default']),
        ]

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

    # =========================================================
    # TEMPLATE RENDERING
    # =========================================================

    def render(self, context):
        """
        Render template using Django template engine.
        """

        subject_template = Template(self.subject)
        rendered_subject = subject_template.render(Context(context))

        html_template = Template(self.html_content)
        rendered_html = html_template.render(Context(context))

        if self.text_content:
            text_template = Template(self.text_content)
            rendered_text = text_template.render(Context(context))
        else:
            rendered_text = re.sub(r'<[^>]+>', '', rendered_html)

        return {
            'subject': rendered_subject,
            'html_content': rendered_html,
            'text_content': rendered_text,
        }

    # =========================================================
    # USAGE TRACKING
    # =========================================================

    def increment_usage(self):
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class Campaign(TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # =========================================================
    # BASIC INFO
    # =========================================================

    name = models.CharField(max_length=255)

    subject = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='campaigns'
    )

    template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='campaigns'
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =========================================================
    # CUSTOM CONTENT
    # =========================================================

    custom_html_content = models.TextField(blank=True)

    custom_text_content = models.TextField(blank=True)

    # =========================================================
    # ANALYTICS
    # =========================================================

    total_sent = models.IntegerField(default=0)

    total_opens = models.IntegerField(default=0)

    total_clicks = models.IntegerField(default=0)

    total_bounces = models.IntegerField(default=0)

    total_unsubscribes = models.IntegerField(default=0)

    # =========================================================
    # TARGETING
    # =========================================================

    target_lists = models.ManyToManyField(
        'contacts.ContactList',
        blank=True,
        related_name='campaigns'
    )

    # =========================================================
    # SENDER INFO
    # =========================================================

    from_email = models.EmailField(blank=True)

    from_name = models.CharField(max_length=255, blank=True)

    reply_to = models.EmailField(blank=True)

    # =========================================================
    # A/B TESTING
    # =========================================================

    is_ab_test = models.BooleanField(default=False)

    ab_variant_b = models.TextField(blank=True)

    ab_winner_criteria = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('opens', 'Open Rate'),
            ('clicks', 'Click Rate'),
        ]
    )

    def __str__(self):
        return self.name

    # =========================================================
    # CAMPAIGN RENDERING
    # =========================================================

    def get_rendered_content(self, contact):
        context = {
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'email': contact.email,
            'company_name': contact.metadata.get('company_name', ''),
        }

        if self.template:
            return self.template.render(context)

        subject_template = Template(self.subject)

        html_template = Template(self.custom_html_content)

        return {
            'subject': subject_template.render(Context(context)),
            'html_content': html_template.render(Context(context)),
            'text_content': self.custom_text_content,
        }