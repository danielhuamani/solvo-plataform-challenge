from django.contrib import admin

from apps.devices.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "platform_user",
        "name",
        "ip_address",
        "is_active",
        "last_seen",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "ip_address", "platform_user__email")
