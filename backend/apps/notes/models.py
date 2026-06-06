from django.db import models


class Note(models.Model):
    """Learning notes with hierarchical structure."""
    class Status(models.IntegerChoices):
        DRAFT = 0, '草稿'
        PUBLISHED = 1, '已发布'

    class LearningStage(models.IntegerChoices):
        BEGINNER = 1, '入门'
        INTERMEDIATE = 2, '进阶'
        ADVANCED = 3, '精通'

    class Difficulty(models.IntegerChoices):
        BEGINNER = 1, '入门'
        INTERMEDIATE = 2, '中级'
        ADVANCED = 3, '高级'

    title = models.CharField(max_length=100, verbose_name='笔记标题')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='笔记别名')
    content = models.TextField(verbose_name='笔记内容(Markdown)')
    category = models.ForeignKey('projects.Category', on_delete=models.CASCADE,
                                 related_name='notes', verbose_name='分类')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE,
                               related_name='notes', verbose_name='作者')
    tags = models.ManyToManyField('projects.Tag', through='NoteTag',
                                  related_name='notes', verbose_name='标签')
    learning_stage = models.IntegerField(choices=LearningStage.choices, default=LearningStage.BEGINNER,
                                         verbose_name='学习阶段')
    progress = models.IntegerField(default=0, verbose_name='学习进度(0-100)')
    difficulty = models.IntegerField(choices=Difficulty.choices, null=True, blank=True,
                                     verbose_name='难度等级')
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞次数')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name='父笔记')
    sort_order = models.IntegerField(default=0, verbose_name='排序权重')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')

    class Meta:
        db_table = 'notes'
        verbose_name = '学习笔记'
        verbose_name_plural = '学习笔记'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['author']),
            models.Index(fields=['learning_stage']),
            models.Index(fields=['parent']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title


class NoteTag(models.Model):
    """Many-to-many relationship for notes and tags."""
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note_tags')
    tag = models.ForeignKey('projects.Tag', on_delete=models.CASCADE, related_name='note_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'note_tags'
        unique_together = ('note', 'tag')
        indexes = [
            models.Index(fields=['note']),
            models.Index(fields=['tag']),
        ]
