from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    EmailVerificationToken,
    PasswordResetToken,
    UserActivityLog,
    UserSession,
)
from .tokens import AccountTokenService

User = get_user_model()


class RequestMetaService:
    @staticmethod
    def get_ip(request):
        if not request:
            return None

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def get_user_agent(request):
        if not request:
            return ""
        return request.META.get("HTTP_USER_AGENT", "")

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

    @staticmethod
    def detect_device(user_agent):
        ua = (user_agent or "").lower()

        if "mobile" in ua or "android" in ua or "iphone" in ua:
            return "Mobile"
        if "ipad" in ua or "tablet" in ua:
            return "Tablet"
        if ua:
            return "Desktop"

        return ""


class AccountActivityService:
    @staticmethod
    def log(user, action, request=None, organization=None, description="", metadata=None):
        if not user or not getattr(user, "is_authenticated", False):
            return None

        return UserActivityLog.objects.create(
            user=user,
            organization=organization or getattr(user, "active_organization", None),
            action=action,
            description=description,
            metadata=metadata or {},
            ip_address=RequestMetaService.get_ip(request),
            user_agent=RequestMetaService.get_user_agent(request),
        )


class AccountSessionService:
    @staticmethod
    def create_session(user, request=None, session_key=""):
        user_agent = RequestMetaService.get_user_agent(request)

        return UserSession.objects.create(
            user=user,
            session_key=session_key or "",
            ip_address=RequestMetaService.get_ip(request),
            user_agent=user_agent,
            device_name=RequestMetaService.detect_device(user_agent),
            browser=RequestMetaService.detect_browser(user_agent),
            os=RequestMetaService.detect_os(user_agent),
            is_active=True,
        )

    @staticmethod
    def touch_user(user, request=None):
        fields = ["last_seen_at"]

        user.last_seen_at = timezone.now()

        ip = RequestMetaService.get_ip(request)
        ua = RequestMetaService.get_user_agent(request)

        if ip:
            user.last_login_ip = ip
            fields.append("last_login_ip")

        if ua:
            user.last_login_user_agent = ua
            fields.append("last_login_user_agent")

        user.save(update_fields=fields)


class AccountTokenManager:
    @staticmethod
    def create_email_verification_token(user, request=None, hours=24):
        raw_token = AccountTokenService.generate_raw_token()
        token_hash = AccountTokenService.hash_token(raw_token)

        EmailVerificationToken.objects.create(
            user=user,
            email=user.email,
            token_hash=token_hash,
            expires_at=AccountTokenService.expiry(hours=hours),
            ip_address=RequestMetaService.get_ip(request),
            user_agent=RequestMetaService.get_user_agent(request),
        )

        return raw_token

    @staticmethod
    def verify_email_token(raw_token):
        token_hash = AccountTokenService.hash_token(raw_token)

        token = (
            EmailVerificationToken.objects
            .select_related("user")
            .filter(token_hash=token_hash)
            .order_by("-created_at")
            .first()
        )

        if not token:
            return False, "Invalid verification token.", None

        if not token.is_valid:
            return False, "Verification token expired or already used.", token.user

        user = token.user
        user.email_verified = True
        user.save(update_fields=["email_verified"])

        token.used_at = timezone.now()
        token.save(update_fields=["used_at"])

        return True, "Email verified successfully.", user

    @staticmethod
    def create_password_reset_token(user, request=None, hours=2):
        raw_token = AccountTokenService.generate_raw_token()
        token_hash = AccountTokenService.hash_token(raw_token)

        PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=AccountTokenService.expiry(hours=hours),
            ip_address=RequestMetaService.get_ip(request),
            user_agent=RequestMetaService.get_user_agent(request),
        )

        return raw_token

    @staticmethod
    def reset_password(raw_token, new_password):
        token_hash = AccountTokenService.hash_token(raw_token)

        token = (
            PasswordResetToken.objects
            .select_related("user")
            .filter(token_hash=token_hash)
            .order_by("-created_at")
            .first()
        )

        if not token:
            return False, "Invalid password reset token.", None

        if not token.is_valid:
            return False, "Password reset token expired or already used.", token.user

        user = token.user
        user.set_password(new_password)
        user.password_changed_at = timezone.now()
        user.save(update_fields=["password", "password_changed_at"])

        token.used_at = timezone.now()
        token.save(update_fields=["used_at"])

        return True, "Password reset successfully.", user


class AccountProfileService:
    @staticmethod
    def update_avatar(user, avatar_file, request=None):
        if user.avatar:
            user.avatar.delete(save=False)

        user.avatar = avatar_file
        user.save(update_fields=["avatar"])

        AccountActivityService.log(
            user=user,
            action="upload_avatar",
            request=request,
            description="User uploaded profile picture.",
        )

        return user

    @staticmethod
    def remove_avatar(user, request=None):
        if user.avatar:
            user.avatar.delete(save=False)

        user.avatar = None
        user.save(update_fields=["avatar"])

        AccountActivityService.log(
            user=user,
            action="remove_avatar",
            request=request,
            description="User removed profile picture.",
        )

        return user
