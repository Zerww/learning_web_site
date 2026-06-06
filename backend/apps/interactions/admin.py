from django.contrib import admin

from apps.interactions.models import Favorite, Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'user', 'created_at']
    list_filter = ['content_type']
    raw_id_fields = ['user']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'user', 'folder_name', 'created_at']
    list_filter = ['content_type']
    raw_id_fields = ['user']
