from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    class Role(models.IntegerChoices):
        VISITOR = 0, '访客'
        ADMIN = 1, '管理员'

    class Status(models.IntegerChoices):
        DISABLED = 0, '禁用'
        NORMAL = 1, '正常'

    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    email = models.EmailField(max_length=100, unique=True, verbose_name='邮箱')
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称')
    avatar = models.URLField(max_length=255, null=True, blank=True, verbose_name='头像URL')
    bio = models.TextField(null=True, blank=True, verbose_name='个人简介')
    role = models.IntegerField(choices=Role.choices, default=Role.VISITOR, verbose_name='角色')
    status = models.IntegerField(choices=Status.choices, default=Status.NORMAL, verbose_name='状态')
    github_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='GitHub链接')
    website_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='个人网站')
    last_login_at = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # Remove unused fields from AbstractUser
    first_name = None
    last_name = None
    date_joined = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.nickname or self.username
