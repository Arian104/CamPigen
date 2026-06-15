import html
import secrets
from html.parser import HTMLParser
from urllib.parse import urlparse

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import TrackedLink, LinkClick


class LinkService:
    @staticmethod
    def generate_tracking_code(length=10):
        while True:
            code = secrets.token_urlsafe(length).replace("-", "").replace("_", "")[:length]
            if not TrackedLink.objects.filter(tracking_code=code).exists():
                return code

    @staticmethod
    def get_public_base_url():
        return (
            getattr(settings, "PUBLIC_APP_BASE_URL", "")
            or getattr(settings, "BACKEND_PUBLIC_URL", "")
            or "http://127.0.0.1:8000"
        ).rstrip("/")

    @classmethod
    def build_tracking_url(cls, tracking_code):
        return f"{cls.get_public_base_url()}/r/{tracking_code}/"

    @classmethod
    def create_tracked_link(
        cls,
        organization,
        original_url,
        name="",
        campaign=None,
        template=None,
        email_job=None,
        contact=None,
        expires_at=None,
        metadata=None,
    ):
        tracking_code = cls.generate_tracking_code()

        return TrackedLink.objects.create(
            organization=organization,
            campaign=campaign,
            template=template,
            email_job=email_job,
            contact=contact,
            name=name,
            original_url=original_url,
            tracking_code=tracking_code,
            expires_at=expires_at,
            metadata=metadata or {},
        )

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def detect_device(user_agent):
        ua = (user_agent or "").lower()

        if "mobile" in ua or "android" in ua or "iphone" in ua:
            return "mobile"
        if "ipad" in ua or "tablet" in ua:
            return "tablet"
        if ua:
            return "desktop"
        return ""

    @staticmethod
    def detect_browser(user_agent):
        ua = (user_agent or "").lower()

        if "edg/" in ua:
            return "Edge"
        if "chrome/" in ua:
            return "Chrome"
        if "safari/" in ua and "chrome/" not in ua:
            return "Safari"
        if "firefox/" in ua:
            return "Firefox"
        return ""

    @staticmethod
    def detect_os(user_agent):
        ua = (user_agent or "").lower()

        if "windows" in ua:
            return "Windows"
        if "mac os" in ua or "macintosh" in ua:
            return "macOS"
        if "android" in ua:
            return "Android"
        if "iphone" in ua or "ipad" in ua:
            return "iOS"
        if "linux" in ua:
            return "Linux"
        return ""

    @classmethod
    @transaction.atomic
    def record_click(cls, tracked_link, request):
        ip_address = cls.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        referrer = request.META.get("HTTP_REFERER", "")

        is_unique = not LinkClick.objects.filter(
            tracked_link=tracked_link,
            ip_address=ip_address,
            user_agent=user_agent,
        ).exists()

        click = LinkClick.objects.create(
            tracked_link=tracked_link,
            organization=tracked_link.organization,
            campaign=tracked_link.campaign,
            email_job=tracked_link.email_job,
            contact=tracked_link.contact,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            device_type=cls.detect_device(user_agent),
            browser=cls.detect_browser(user_agent),
            os=cls.detect_os(user_agent),
            is_unique=is_unique,
            metadata={
                "path": request.path,
                "query_string": request.META.get("QUERY_STRING", ""),
            },
        )

        TrackedLink.objects.filter(id=tracked_link.id).update(
            click_count=F("click_count") + 1,
            unique_click_count=F("unique_click_count") + (1 if is_unique else 0),
            last_clicked_at=timezone.now(),
        )

        return click

    @staticmethod
    def is_safe_redirect_url(url):
        parsed = urlparse(url)
        return parsed.scheme in ["http", "https"] and bool(parsed.netloc)


class _EmailLinkHTMLRewriter(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self, job):
        super().__init__(convert_charrefs=False)
        self.job = job
        self.output = []
        self.link_index = 0

    def handle_starttag(self, tag, attrs):
        attrs = self._rewrite_attrs(tag, attrs)
        self.output.append(self._build_start_tag(tag, attrs, self_closing=False))

    def handle_startendtag(self, tag, attrs):
        attrs = self._rewrite_attrs(tag, attrs)
        self.output.append(self._build_start_tag(tag, attrs, self_closing=True))

    def handle_endtag(self, tag):
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        self.output.append(data)

    def handle_entityref(self, name):
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        self.output.append(f"&#{name};")

    def handle_comment(self, data):
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")

    def unknown_decl(self, data):
        self.output.append(f"<![{data}]>")

    def get_html(self):
        return "".join(self.output)

    def _rewrite_attrs(self, tag, attrs):
        if tag.lower() != "a":
            return attrs

        rewritten = []
        href_found = False

        for key, value in attrs:
            if key and key.lower() == "href":
                href_found = True
                value = LinkRewriteService.rewrite_href(
                    job=self.job,
                    original_href=value or "",
                    link_index=self.link_index,
                )
                self.link_index += 1

            rewritten.append((key, value))

        if not href_found:
            return attrs

        return rewritten

    def _build_start_tag(self, tag, attrs, self_closing=False):
        rendered_attrs = []

        for key, value in attrs:
            if value is None:
                rendered_attrs.append(html.escape(str(key), quote=True))
            else:
                rendered_attrs.append(
                    f'{html.escape(str(key), quote=True)}="{html.escape(str(value), quote=True)}"'
                )

        attrs_text = f" {' '.join(rendered_attrs)}" if rendered_attrs else ""

        if self_closing:
            return f"<{tag}{attrs_text} />"

        return f"<{tag}{attrs_text}>"


class LinkRewriteService:
    SKIP_SCHEMES = {"mailto", "tel", "sms", "javascript", "data"}
    SKIP_KEYWORDS = {
        "unsubscribe",
        "manage-preferences",
        "preference-center",
        "preferences",
        "opt-out",
        "optout",
    }

    @classmethod
    def rewrite_email_html(cls, job):
        if not job or not getattr(job, "html_body", ""):
            return getattr(job, "html_body", "")

        parser = _EmailLinkHTMLRewriter(job)
        parser.feed(job.html_body)
        parser.close()

        return parser.get_html()

    @classmethod
    def rewrite_href(cls, job, original_href, link_index=0):
        href = (original_href or "").strip()

        if not href:
            return original_href

        if cls.should_skip_url(href):
            return original_href

        organization = getattr(job, "organization", None) or (
            getattr(getattr(job, "campaign", None), "organization", None)
        )

        if not organization:
            return original_href

        tracked_link = LinkService.create_tracked_link(
            organization=organization,
            original_url=href,
            name=cls.build_link_name(job, href, link_index),
            campaign=getattr(job, "campaign", None),
            template=None,
            email_job=job,
            contact=getattr(job, "contact", None),
            metadata={
                "source": "email_engine",
                "link_index": link_index,
                "recipient_email": getattr(job, "recipient_email", ""),
                "email_type": getattr(job, "email_type", ""),
                "subject": getattr(job, "subject_snapshot", ""),
            },
        )

        return LinkService.build_tracking_url(tracked_link.tracking_code)

    @classmethod
    def should_skip_url(cls, url):
        lowered = (url or "").strip().lower()

        if not lowered:
            return True

        if lowered.startswith("#"):
            return True

        if lowered.startswith("/r/"):
            return True

        public_base = LinkService.get_public_base_url().lower().rstrip("/")
        if lowered.startswith(f"{public_base}/r/"):
            return True

        parsed = urlparse(lowered)

        if parsed.scheme in cls.SKIP_SCHEMES:
            return True

        if parsed.scheme not in ["http", "https"]:
            return True

        for keyword in cls.SKIP_KEYWORDS:
            if keyword in lowered:
                return True

        return not LinkService.is_safe_redirect_url(url)

    @staticmethod
    def build_link_name(job, href, link_index):
        campaign = getattr(job, "campaign", None)
        campaign_name = getattr(campaign, "name", "") if campaign else ""

        if campaign_name:
            return f"{campaign_name} - Link {link_index + 1}"

        subject = getattr(job, "subject_snapshot", "") or "Email"
        return f"{subject[:80]} - Link {link_index + 1}"
