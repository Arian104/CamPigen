from django.conf import settings


class AccountEmailBuilder:
    @staticmethod
    def get_frontend_base_url():
        return getattr(settings, "FRONTEND_BASE_URL", "http://localhost:3000").rstrip("/")

    @classmethod
    def verification_url(cls, token):
        return f"{cls.get_frontend_base_url()}/verify-email?token={token}"

    @classmethod
    def password_reset_url(cls, token):
        return f"{cls.get_frontend_base_url()}/reset-password?token={token}"

    @classmethod
    def verification_email(cls, user, token):
        url = cls.verification_url(token)

        subject = "Verify your email address"

        text = f"""
Hi {user.first_name or user.username},

Please verify your email address by opening this link:

{url}

If you did not create this account, you can ignore this email.
"""

        html = f"""
<div style="font-family:Arial,sans-serif;max-width:620px;margin:auto;padding:24px;">
  <h2>Verify your email address</h2>
  <p>Hi {user.first_name or user.username},</p>
  <p>Please verify your email address to activate your account.</p>
  <p>
    <a href="{url}" style="display:inline-block;background:#4f46e5;color:#ffffff;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:bold;">
      Verify Email
    </a>
  </p>
  <p>If the button does not work, copy and paste this link:</p>
  <p>{url}</p>
</div>
"""

        return subject, text, html

    @classmethod
    def password_reset_email(cls, user, token):
        url = cls.password_reset_url(token)

        subject = "Reset your password"

        text = f"""
Hi {user.first_name or user.username},

You requested a password reset. Open this link to set a new password:

{url}

If you did not request this, you can ignore this email.
"""

        html = f"""
<div style="font-family:Arial,sans-serif;max-width:620px;margin:auto;padding:24px;">
  <h2>Reset your password</h2>
  <p>Hi {user.first_name or user.username},</p>
  <p>Open the link below to set a new password.</p>
  <p>
    <a href="{url}" style="display:inline-block;background:#4f46e5;color:#ffffff;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:bold;">
      Reset Password
    </a>
  </p>
  <p>If the button does not work, copy and paste this link:</p>
  <p>{url}</p>
</div>
"""

        return subject, text, html
