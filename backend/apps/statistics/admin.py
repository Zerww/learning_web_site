from django.contrib import admin

from apps.statistics.models import VisitLog


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'request_url', 'request_method',
                    'response_status', 'device_type', 'created_at']
    list_filter = ['request_method', 'device_type', 'content_type']
    search_fields = ['ip_address', 'request_url']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
