from django.db import models


class Setting(models.Model):
    """System configuration key-value store."""
    key = models.CharField(max_length=50, unique=True, verbose_name='配置键名')
    value = models.TextField(verbose_name='配置值')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='配置描述')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'settings'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'

    def __str__(self):
        return self.key
