from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import UserActivityLog, UserSession

User = get_user_model()


class ActiveOrganizationSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    subdomain = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, allow_blank=True)


class UserProfileSerializer(serializers.ModelSerializer):
    avatar_display_url = serializers.CharField(read_only=True)
    active_organization_detail = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "phone",
            "job_title",
            "department",
            "avatar",
            "avatar_url",
            "avatar_display_url",
            "email_verified",
            "timezone",
            "language",
            "date_format",
            "time_format",
            "theme_mode",
            "accent_color",
            "sidebar_collapsed",
            "default_dashboard",
            "preferences",
            "notification_preferences",
            "active_organization",
            "active_organization_detail",
            "is_staff",
            "last_seen_at",
            "last_login_ip",
            "password_changed_at",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "email",
            "avatar",
            "avatar_display_url",
            "email_verified",
            "active_organization",
            "active_organization_detail",
            "is_staff",
            "last_seen_at",
            "last_login_ip",
            "password_changed_at",
            "date_joined",
        ]

    def get_active_organization_detail(self, obj):
        org = obj.active_organization

        if not org:
            return None

        membership = obj.organization_memberships.filter(organization=org).first()

        return {
            "id": str(org.id),
            "name": org.name,
            "subdomain": getattr(org, "subdomain", ""),
            "role": membership.role if membership else "",
        }


class UserAvatarUploadSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=True)

    def validate_avatar(self, value):
        max_size = 2 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError("Avatar image must be smaller than 2 MB.")

        allowed_types = ["image/jpeg", "image/png", "image/webp"]

        if getattr(value, "content_type", "") not in allowed_types:
            raise serializers.ValidationError("Only JPEG, PNG, and WEBP images are allowed.")

        return value


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "timezone",
            "language",
            "date_format",
            "time_format",
            "theme_mode",
            "accent_color",
            "sidebar_collapsed",
            "default_dashboard",
            "preferences",
            "notification_preferences",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.email = user.email.lower().strip()
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower().strip()
        password = attrs["password"]

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active or user.is_deleted:
            raise serializers.ValidationError("This account is not active.")

        if user.is_locked:
            raise serializers.ValidationError("This account is temporarily locked.")

        attrs["user"] = user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})

        return attrs


class EmailVerificationRequestSerializer(serializers.Serializer):
    pass


class EmailVerificationConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})

        return attrs


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = [
            "id",
            "session_key",
            "ip_address",
            "user_agent",
            "device_name",
            "browser",
            "os",
            "country",
            "city",
            "is_active",
            "last_activity_at",
            "revoked_at",
            "revoked_reason",
            "created_at",
        ]
        read_only_fields = fields


class UserActivityLogSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = UserActivityLog
        fields = [
            "id",
            "organization",
            "organization_name",
            "action",
            "description",
            "metadata",
            "ip_address",
            "user_agent",
            "created_at",
        ]
        read_only_fields = fields


class BasicUserSerializer(serializers.ModelSerializer):
    avatar_display_url = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "avatar_display_url",
            "email_verified",
            "is_staff",
        ]
        read_only_fields = fields
