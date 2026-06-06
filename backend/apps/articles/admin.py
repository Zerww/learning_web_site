from django.contrib import admin

from apps.articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'status', 'is_featured', 'is_top',
                    'view_count', 'like_count', 'comment_count', 'published_at']
    list_filter = ['status', 'is_featured', 'is_top', 'source_type']
    search_fields = ['title', 'summary']
    readonly_fields = ['reading_time', 'word_count', 'view_count', 'like_count',
                       'favorite_count', 'comment_count', 'created_at', 'updated_at']
    raw_id_fields = ['category', 'author']
    date_hierarchy = 'published_at'
