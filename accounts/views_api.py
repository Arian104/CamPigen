from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserActivityLog, UserSession
from .serializers import (
    BasicUserSerializer,
    ChangePasswordSerializer,
    EmailVerificationConfirmSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserActivityLogSerializer,
    UserAvatarUploadSerializer,
    UserPreferencesSerializer,
    UserProfileSerializer,
    UserSessionSerializer,
)
from .services import (
    AccountActivityService,
    AccountProfileService,
    AccountSessionService,
    AccountTokenManager,
)
from .tasks import send_email_verification_task, send_password_reset_task

User = get_user_model()


def token_response_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": BasicUserSerializer(user).data,
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    raw_token = AccountTokenManager.create_email_verification_token(user, request=request)
    send_email_verification_task.delay(str(user.id), raw_token)

    AccountActivityService.log(
        user=user,
        action="register",
        request=request,
        description="User registered.",
    )

    return Response(
        {
            "message": "Account created. Verification email has been sent.",
            "user": BasicUserSerializer(user).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data, context={"request": request})

    if not serializer.is_valid():
        email = request.data.get("email", "")
        user = User.objects.filter(email=email).first()

        if user:
            user.failed_login_attempts += 1
            user.save(update_fields=["failed_login_attempts"])

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data["user"]

    user.failed_login_attempts = 0
    user.last_seen_at = timezone.now()
    user.save(update_fields=["failed_login_attempts", "last_seen_at"])

    AccountSessionService.create_session(user, request=request)
    AccountSessionService.touch_user(user, request=request)

    AccountActivityService.log(
        user=user,
        action="login",
        request=request,
        description="User logged in.",
    )

    return Response(token_response_for_user(user))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    AccountActivityService.log(
        user=request.user,
        action="logout",
        request=request,
        description="User logged out.",
    )

    UserSession.objects.filter(user=request.user, is_active=True).update(
        is_active=False,
        revoked_at=timezone.now(),
        revoked_reason="logout",
    )

    return Response({"message": "Logged out successfully."})


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET":
        return Response(UserProfileSerializer(request.user).data)

    serializer = UserProfileSerializer(
        request.user,
        data=request.data,
        partial=True,
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    AccountActivityService.log(
        user=request.user,
        action="update_profile",
        request=request,
        description="User updated profile.",
    )

    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_preferences(request):
    serializer = UserPreferencesSerializer(
        request.user,
        data=request.data,
        partial=True,
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    AccountActivityService.log(
        user=request.user,
        action="update_profile",
        request=request,
        description="User updated preferences.",
    )

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    serializer = UserAvatarUploadSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = AccountProfileService.update_avatar(
        request.user,
        serializer.validated_data["avatar"],
        request=request,
    )

    return Response(UserProfileSerializer(user).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_avatar(request):
    user = AccountProfileService.remove_avatar(request.user, request=request)
    return Response(UserProfileSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={"request": request})

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    user.set_password(serializer.validated_data["new_password"])
    user.password_changed_at = timezone.now()
    user.save(update_fields=["password", "password_changed_at"])

    AccountActivityService.log(
        user=user,
        action="change_password",
        request=request,
        description="User changed password.",
    )

    return Response({"message": "Password changed successfully."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_verification_email(request):
    user = request.user

    if user.email_verified:
        return Response({"message": "Email is already verified."})

    raw_token = AccountTokenManager.create_email_verification_token(user, request=request)
    send_email_verification_task.delay(str(user.id), raw_token)

    return Response({"message": "Verification email sent."})


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email(request):
    serializer = EmailVerificationConfirmSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    success, message, user = AccountTokenManager.verify_email_token(
        serializer.validated_data["token"]
    )

    if user:
        AccountActivityService.log(
            user=user,
            action="verify_email",
            request=request,
            description=message,
        )

    return Response(
        {"success": success, "message": message},
        status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"].lower().strip()
    user = User.objects.filter(email=email, is_active=True, is_deleted=False).first()

    if user:
        raw_token = AccountTokenManager.create_password_reset_token(user, request=request)
        send_password_reset_task.delay(str(user.id), raw_token)

        AccountActivityService.log(
            user=user,
            action="request_password_reset",
            request=request,
            description="User requested password reset.",
        )

    return Response({
        "message": "If an account exists for this email, a reset link has been sent."
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    success, message, user = AccountTokenManager.reset_password(
        serializer.validated_data["token"],
        serializer.validated_data["new_password"],
    )

    if user:
        AccountActivityService.log(
            user=user,
            action="reset_password",
            request=request,
            description=message,
        )

    return Response(
        {"success": success, "message": message},
        status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sessions(request):
    rows = UserSession.objects.filter(user=request.user).order_by("-last_activity_at")[:50]
    return Response(UserSessionSerializer(rows, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revoke_session(request, session_id):
    session = UserSession.objects.filter(id=session_id, user=request.user).first()

    if not session:
        return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

    session.revoke(reason="manual_revoke")

    AccountActivityService.log(
        user=request.user,
        action="session_revoked",
        request=request,
        description="User revoked a session.",
        metadata={"session_id": str(session.id)},
    )

    return Response({"message": "Session revoked."})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activity(request):
    rows = UserActivityLog.objects.filter(user=request.user).order_by("-created_at")[:100]
    return Response(UserActivityLogSerializer(rows, many=True).data)
