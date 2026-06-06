from django.contrib import admin

from apps.settings.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'value', 'is_public', 'updated_at']
    list_filter = ['is_public']
    search_fields = ['key', 'description']
