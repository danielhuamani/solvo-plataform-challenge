from django.contrib import admin

from apps.platforms.models import Platform, PlatformSetting


class PlatformSettingInline(admin.StackedInline):
    model = PlatformSetting
    extra = 0
    max_num = 1
    can_delete = False


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    inlines = (PlatformSettingInline,)


@admin.register(PlatformSetting)
class PlatformSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'max_devices', 'allow_inactive_login', 'created_at')
    list_filter = ('allow_inactive_login',)
