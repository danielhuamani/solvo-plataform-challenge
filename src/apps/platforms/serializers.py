from rest_framework import serializers

from apps.platforms.models import Platform


class PlatformListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ("name", "slug")
