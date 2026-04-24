from django.db import models

from apps.accounts.models import PlatformUser


class Device(models.Model):
    platform_user = models.ForeignKey(
        PlatformUser,
        on_delete=models.CASCADE,
        related_name="devices",
    )

    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.platform_user.email})"
