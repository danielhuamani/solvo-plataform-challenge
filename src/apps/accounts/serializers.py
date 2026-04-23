from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import PlatformUser
from apps.notifications.services import notify_user_registered
from apps.platforms.models import Platform, PlatformSetting


class PlatformUserRegisterSerializer(serializers.Serializer):
    platform_slug = serializers.SlugField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        platform_slug = attrs['platform_slug']
        try:
            platform = Platform.objects.get(slug=platform_slug)
        except Platform.DoesNotExist:
            raise serializers.ValidationError({'platform_slug': 'Platform not found.'})

        if not platform.is_active:
            raise serializers.ValidationError({'platform_slug': 'Platform is inactive.'})

        attrs['platform'] = platform
        return attrs

    def create(self, validated_data):
        platform = validated_data['platform']
        email = validated_data['email'].lower()

        user = PlatformUser(
            platform=platform,
            email=email,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=True,
        )
        user.set_password(validated_data['password'])

        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError({'email': 'Email already registered for this platform.'})

        notify_user_registered(
            platform_slug=platform.slug,
            platform_user_id=user.id,
            email=user.email,
        )

        return user


class PlatformUserLoginSerializer(serializers.Serializer):
    platform_slug = serializers.SlugField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        platform_slug = attrs['platform_slug']
        email = attrs['email'].lower()
        password = attrs['password']

        try:
            platform = Platform.objects.get(slug=platform_slug)
        except Platform.DoesNotExist:
            raise serializers.ValidationError({'platform_slug': 'Platform not found.'})

        if not platform.is_active:
            raise serializers.ValidationError({'platform_slug': 'Platform is inactive.'})

        try:
            settings = platform.settings
        except PlatformSetting.DoesNotExist:
            settings = None

        try:
            user = PlatformUser.objects.get(platform=platform, email=email)
        except PlatformUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'Invalid credentials.'})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid credentials.'})

        if settings is not None and not settings.allow_inactive_login and not user.is_active:
            raise serializers.ValidationError({'email': 'User is inactive.'})

        refresh = RefreshToken.for_user(user)
        refresh['platform_user_id'] = user.id
        refresh['platform_id'] = platform.id
        refresh['platform_slug'] = platform.slug
        refresh['email'] = user.email

        access = refresh.access_token
        access['platform_user_id'] = user.id
        access['platform_id'] = platform.id
        access['platform_slug'] = platform.slug
        access['email'] = user.email

        attrs['refresh'] = str(refresh)
        attrs['access'] = str(access)
        return attrs
