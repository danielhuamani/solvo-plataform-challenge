from rest_framework import serializers

from apps.core.utils import now_local
from apps.devices.models import Device
from apps.devices.services import enforce_device_limit
from apps.core.utils import get_client_ip


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "name",
            "ip_address",
            "is_active",
            "last_seen",
            "created_at",
            "updated_at",
        )


class DeviceCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(required=False, default=True)
    last_seen = serializers.DateTimeField(required=False)

    def validate(self, attrs):
        platform = self.context["platform"]
        platform_user = self.context["platform_user"]

        platform_settings = getattr(platform, "settings", None)
        max_devices = getattr(platform_settings, "max_devices", 5)
        enforce_device_limit(platform_user=platform_user, max_devices=max_devices)

        return attrs

    def validate_last_seen(self, value):
        return value

    def create(self, validated_data):
        platform_user = self.context["platform_user"]
        last_seen = validated_data.get("last_seen") or now_local()

        request = self.context.get("request")
        ip_address = get_client_ip(request) if request is not None else None

        if not ip_address:
            raise serializers.ValidationError(
                {"ip_address": "Could not infer IP address from request."}
            )

        ip_address = serializers.IPAddressField().run_validation(ip_address)

        device = Device.objects.create(
            platform_user=platform_user,
            name=validated_data["name"],
            ip_address=ip_address,
            is_active=validated_data.get("is_active", True),
            last_seen=last_seen,
        )
        return device
