from django.db import models


class Comment(models.Model):
    """Comments on articles, projects, and notes."""
    class ContentType(models.IntegerChoices):
        ARTICLE = 1, '文章'
        PROJECT = 2, '项目'
        NOTE = 3, '笔记'

    class Status(models.IntegerChoices):
        PENDING = 0, '待审核'
        APPROVED = 1, '已发布'
        REJECTED = 2, '已拒绝'

    content = models.TextField(verbose_name='评论内容')
    content_type = models.IntegerField(choices=ContentType.choices, verbose_name='评论对象类型')
    object_id = models.BigIntegerField(verbose_name='评论对象ID')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='comments', verbose_name='评论用户')
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='访客昵称')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='访客邮箱')
    website = models.URLField(max_length=255, null=True, blank=True, verbose_name='访客网站')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies', verbose_name='父评论')
    reply_to_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='replied_comments', verbose_name='回复用户')
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING, verbose_name='状态')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    like_count = models.IntegerField(default=0, verbose_name='点赞次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = '评论'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
            models.Index(fields=['parent']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.get_content_type_display()}#{self.object_id} - {self.content[:30]}'
