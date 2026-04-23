from django.db import models

from uuslug import uuslug


class Platform(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = uuslug(self.name, instance=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.slug})"


class PlatformSetting(models.Model):
    platform = models.OneToOneField(
        Platform,
        on_delete=models.CASCADE,
        related_name='settings',
    )

    max_devices = models.PositiveIntegerField(default=5)
    allow_inactive_login = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.platform.slug}"
