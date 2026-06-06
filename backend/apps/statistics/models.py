from django.db import models


class VisitLog(models.Model):
    """Website visit log for analytics."""
    class DeviceType(models.IntegerChoices):
        PC = 1, 'PC'
        MOBILE = 2, '移动端'
        TABLET = 3, '平板'

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='visit_logs', verbose_name='用户')
    session_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='会话ID')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户代理')
    referer = models.URLField(max_length=255, null=True, blank=True, verbose_name='来源页面')
    request_url = models.CharField(max_length=255, verbose_name='访问URL')
    request_method = models.CharField(max_length=10, verbose_name='请求方法')
    response_status = models.IntegerField(null=True, blank=True, verbose_name='响应状态码')
    content_type = models.IntegerField(null=True, blank=True, verbose_name='内容类型')
    object_id = models.BigIntegerField(null=True, blank=True, verbose_name='内容对象ID')
    device_type = models.IntegerField(choices=DeviceType.choices, null=True, blank=True,
                                      verbose_name='设备类型')
    browser = models.CharField(max_length=50, null=True, blank=True, verbose_name='浏览器')
    os = models.CharField(max_length=50, null=True, blank=True, verbose_name='操作系统')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='国家')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='城市')
    duration = models.IntegerField(null=True, blank=True, verbose_name='停留时间(秒)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')

    class Meta:
        db_table = 'visit_logs'
        verbose_name = '访问日志'
        verbose_name_plural = '访问日志'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['request_url']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['created_at']),
            models.Index(fields=['device_type']),
        ]

    def __str__(self):
        return f'{self.ip_address} -> {self.request_url}'
