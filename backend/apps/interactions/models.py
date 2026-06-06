from django.db import models


class Like(models.Model):
    """Like records for articles, projects, notes, and comments."""
    class ContentType(models.IntegerChoices):
        ARTICLE = 1, '文章'
        PROJECT = 2, '项目'
        NOTE = 3, '笔记'
        COMMENT = 4, '评论'

    content_type = models.IntegerField(choices=ContentType.choices, verbose_name='点赞对象类型')
    object_id = models.BigIntegerField(verbose_name='点赞对象ID')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True,
                             related_name='likes', verbose_name='用户')
    anonymous_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='匿名标识')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'likes'
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['object_id']),
        ]

    def __str__(self):
        return f'{self.get_content_type_display()}#{self.object_id}'


class Favorite(models.Model):
    """Favorite/bookmark records for articles, projects, and notes."""
    class ContentType(models.IntegerChoices):
        ARTICLE = 1, '文章'
        PROJECT = 2, '项目'
        NOTE = 3, '笔记'

    content_type = models.IntegerField(choices=ContentType.choices, verbose_name='收藏对象类型')
    object_id = models.BigIntegerField(verbose_name='收藏对象ID')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='favorites', verbose_name='用户')
    folder_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='收藏夹名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'favorites'
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f'{self.get_content_type_display()}#{self.object_id}'
