from django.urls import path

from . import views_api

urlpatterns = [
    path("register/", views_api.register, name="accounts-register"),
    path("login/", views_api.login, name="accounts-login"),
    path("logout/", views_api.logout, name="accounts-logout"),

    path("me/", views_api.me, name="accounts-me"),
    path("me/preferences/", views_api.update_preferences, name="accounts-preferences"),
    path("me/avatar/", views_api.upload_avatar, name="accounts-upload-avatar"),
    path("me/avatar/remove/", views_api.remove_avatar, name="accounts-remove-avatar"),

    path("change-password/", views_api.change_password, name="accounts-change-password"),

    path("send-verification-email/", views_api.send_verification_email, name="accounts-send-verification-email"),
    path("verify-email/", views_api.verify_email, name="accounts-verify-email"),

    path("request-password-reset/", views_api.request_password_reset, name="accounts-request-password-reset"),
    path("reset-password/", views_api.reset_password, name="accounts-reset-password"),

    path("sessions/", views_api.sessions, name="accounts-sessions"),
    path("sessions/<uuid:session_id>/revoke/", views_api.revoke_session, name="accounts-revoke-session"),

    path("activity/", views_api.activity, name="accounts-activity"),
]
