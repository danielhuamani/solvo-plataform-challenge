from django.contrib import admin

from apps.accounts.models import PlatformUser


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'email', 'is_active', 'created_at')
    list_filter = ('platform', 'is_active')
    search_fields = ('email',)