from django.contrib import admin

from apps.projects.models import Category, Project, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'type', 'sort_order', 'created_at']
    list_filter = ['type']
    search_fields = ['name', 'slug']
    ordering = ['type', 'sort_order']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'color', 'type', 'usage_count']
    list_filter = ['type']
    search_fields = ['name', 'slug']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'status', 'is_featured',
                    'view_count', 'like_count', 'published_at']
    list_filter = ['status', 'is_featured', 'difficulty']
    search_fields = ['title', 'description']
    readonly_fields = ['view_count', 'like_count', 'favorite_count',
                       'created_at', 'updated_at', 'published_at']
    raw_id_fields = ['category', 'author']
