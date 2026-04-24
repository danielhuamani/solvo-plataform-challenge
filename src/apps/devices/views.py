from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.devices.serializers import DeviceCreateSerializer, DeviceSerializer


class DeviceListCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request and self.request.method == 'POST':
            return DeviceCreateSerializer
        return DeviceSerializer

    def get(self, request):
        qs = request.platform_user.devices.all().order_by('-created_at')
        serializer = DeviceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeviceCreateSerializer(
            data=request.data,
            context={'platform_user': request.platform_user, 'platform': request.platform, 'request': request},
        )
        serializer.is_valid(raise_exception=True)
        device = serializer.save()

        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)
