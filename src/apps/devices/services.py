from rest_framework import serializers

from apps.devices.models import Device


def get_client_ip(request) -> str | None:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def enforce_device_limit(*, platform_user, max_devices: int) -> None:
    active_devices_count = Device.objects.filter(platform_user=platform_user, is_active=True).count()
    if active_devices_count >= max_devices:
        raise serializers.ValidationError(
            {
                'detail': f'Max active devices limit reached ({max_devices}).',
            }
        )
