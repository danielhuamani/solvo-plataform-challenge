from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.devices.serializers import DeviceCreateSerializer, DeviceSerializer
from apps.devices.services import enforce_device_limit


class DeviceListCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = request.platform_user.devices.all().order_by('-created_at')
        serializer = DeviceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        platform_settings = getattr(request.platform, 'settings', None)
        max_devices = getattr(platform_settings, 'max_devices', 5)

        enforce_device_limit(platform_user=request.platform_user, max_devices=max_devices)

        serializer = DeviceCreateSerializer(
            data=request.data,
            context={'platform_user': request.platform_user},
        )
        serializer.is_valid(raise_exception=True)
        device = serializer.save()

        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)
