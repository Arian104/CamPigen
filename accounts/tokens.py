import hashlib
import secrets
from datetime import timedelta

from django.utils import timezone


class AccountTokenService:
    @staticmethod
    def generate_raw_token(length=48):
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_token(raw_token):
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @staticmethod
    def expiry(hours=24):
        return timezone.now() + timedelta(hours=hours)
