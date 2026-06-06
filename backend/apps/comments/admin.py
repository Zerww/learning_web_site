from django.contrib import admin

from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'user', 'nickname',
                    'status', 'like_count', 'created_at']
    list_filter = ['content_type', 'status']
    search_fields = ['content']
    raw_id_fields = ['user', 'parent', 'reply_to_user']
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status=1)
    approve_comments.short_description = '审核通过所选评论'

    def reject_comments(self, request, queryset):
        queryset.update(status=2)
    reject_comments.short_description = '拒绝所选评论'
