from rest_framework import generics, permissions

from apps.platforms.models import Platform
from apps.platforms.serializers import PlatformListSerializer


class PlatformListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PlatformListSerializer

    def get_queryset(self):
        return Platform.objects.filter(is_active=True).order_by('name')
