from django.db import models


class Article(models.Model):
    """Technical article / blog post."""
    class Status(models.IntegerChoices):
        DRAFT = 0, '草稿'
        PUBLISHED = 1, '已发布'
        HIDDEN = 2, '隐藏'

    class SourceType(models.IntegerChoices):
        ORIGINAL = 1, '原创'
        TRANSLATION = 2, '翻译'
        REPRINT = 3, '转载'

    title = models.CharField(max_length=150, verbose_name='文章标题')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='文章别名')
    summary = models.CharField(max_length=500, null=True, blank=True, verbose_name='文章摘要')
    content = models.TextField(verbose_name='文章内容(Markdown)')
    cover_image = models.URLField(max_length=255, null=True, blank=True, verbose_name='封面图片')
    category = models.ForeignKey('projects.Category', on_delete=models.CASCADE,
                                 related_name='articles', verbose_name='分类')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE,
                               related_name='articles', verbose_name='作者')
    tags = models.ManyToManyField('projects.Tag', through='ArticleTag',
                                  related_name='articles', verbose_name='标签')
    reading_time = models.IntegerField(default=0, verbose_name='阅读时间(分钟)')
    word_count = models.IntegerField(default=0, verbose_name='字数')
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    allow_comment = models.BooleanField(default=True, verbose_name='允许评论')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞次数')
    favorite_count = models.IntegerField(default=0, verbose_name='收藏次数')
    comment_count = models.IntegerField(default=0, verbose_name='评论次数')
    source_type = models.IntegerField(choices=SourceType.choices, null=True, blank=True,
                                      verbose_name='来源类型')
    source_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='原文链接')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        db_table = 'articles'
        verbose_name = '文章'
        verbose_name_plural = '文章'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['author']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_top']),
            models.Index(fields=['published_at']),
            models.Index(fields=['view_count']),
        ]

    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    """Many-to-many relationship for articles and tags."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_tags')
    tag = models.ForeignKey('projects.Tag', on_delete=models.CASCADE, related_name='article_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_tags'
        unique_together = ('article', 'tag')
        indexes = [
            models.Index(fields=['article']),
            models.Index(fields=['tag']),
        ]
