from django.db import models


class Category(models.Model):
    """Content category for projects, articles, and notes."""
    class Type(models.IntegerChoices):
        PROJECT = 1, '项目'
        ARTICLE = 2, '文章'
        NOTE = 3, '笔记'

    name = models.CharField(max_length=50, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, verbose_name='分类别名')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='分类描述')
    type = models.IntegerField(choices=Type.choices, default=Type.PROJECT, verbose_name='类型')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='父分类')
    sort_order = models.IntegerField(default=0, verbose_name='排序权重')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='图标')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = '分类'
        unique_together = ('slug', 'type')
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag for content labeling."""
    class Type(models.IntegerChoices):
        PROJECT = 1, '项目'
        ARTICLE = 2, '文章'
        NOTE = 3, '笔记'
        GENERAL = 4, '通用'

    name = models.CharField(max_length=30, verbose_name='标签名称')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='标签别名')
    color = models.CharField(max_length=10, default='#409EFF', verbose_name='标签颜色')
    type = models.IntegerField(choices=Type.choices, default=Type.GENERAL, verbose_name='类型')
    usage_count = models.IntegerField(default=0, verbose_name='使用次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'tags'
        verbose_name = '标签'
        verbose_name_plural = '标签'
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['usage_count']),
        ]

    def __str__(self):
        return self.name


class Project(models.Model):
    """Project portfolio item."""
    class Status(models.IntegerChoices):
        DRAFT = 0, '草稿'
        PUBLISHED = 1, '已发布'
        HIDDEN = 2, '隐藏'

    class Difficulty(models.IntegerChoices):
        BEGINNER = 1, '入门'
        INTERMEDIATE = 2, '中级'
        ADVANCED = 3, '高级'

    title = models.CharField(max_length=100, verbose_name='项目名称')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='项目别名')
    description = models.TextField(verbose_name='项目简介')
    content = models.TextField(verbose_name='详细说明(Markdown)')
    cover_image = models.URLField(max_length=255, null=True, blank=True, verbose_name='封面图片')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects',
                                 verbose_name='分类')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='projects',
                               verbose_name='作者')
    tech_stack = models.CharField(max_length=255, null=True, blank=True, verbose_name='技术栈')
    github_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='GitHub链接')
    demo_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='演示地址')
    video_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='演示视频')
    tags = models.ManyToManyField(Tag, through='ProjectTag', related_name='projects',
                                  verbose_name='标签')
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞次数')
    favorite_count = models.IntegerField(default=0, verbose_name='收藏次数')
    difficulty = models.IntegerField(choices=Difficulty.choices, null=True, blank=True,
                                     verbose_name='难度等级')
    start_date = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='完成日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        db_table = 'projects'
        verbose_name = '项目'
        verbose_name_plural = '项目'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['author']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['published_at']),
            models.Index(fields=['view_count']),
        ]

    def __str__(self):
        return self.title


class ProjectTag(models.Model):
    """Many-to-many relationship for projects and tags."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='project_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_tags'
        unique_together = ('project', 'tag')
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['tag']),
        ]
