from django.db import models as db_models
from rest_framework import serializers

from apps.articles.models import Article, ArticleTag
from apps.projects.serializers import CategorySerializer, TagSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    """Article list serializer."""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'summary', 'cover_image', 'category',
                  'tags', 'reading_time', 'word_count', 'status', 'is_featured',
                  'is_top', 'view_count', 'like_count', 'comment_count',
                  'published_at', 'author']

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'nickname': obj.author.nickname or obj.author.username,
            'avatar': obj.author.avatar,
        }


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Article detail serializer."""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    prev_article = serializers.SerializerMethodField()
    next_article = serializers.SerializerMethodField()
    related_articles = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'nickname': obj.author.nickname or obj.author.username,
            'avatar': obj.author.avatar,
        }

    def get_prev_article(self, obj):
        if not obj.published_at:
            return None
        prev = Article.objects.filter(
            status=1, published_at__lt=obj.published_at
        ).order_by('-published_at').first()
        if prev:
            return {'id': prev.id, 'title': prev.title, 'slug': prev.slug}
        return None

    def get_next_article(self, obj):
        if not obj.published_at:
            return None
        next_article = Article.objects.filter(
            status=1, published_at__gt=obj.published_at
        ).order_by('published_at').first()
        if next_article:
            return {'id': next_article.id, 'title': next_article.title, 'slug': next_article.slug}
        return None

    def get_related_articles(self, obj):
        related = Article.objects.filter(
            category=obj.category, status=1
        ).exclude(id=obj.id)[:4]
        return [{'id': a.id, 'title': a.title, 'slug': a.slug} for a in related]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Like
            return Like.objects.filter(content_type=1, object_id=obj.id, user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Favorite
            return Favorite.objects.filter(content_type=1, object_id=obj.id, user=request.user).exists()
        return False


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Article create/update serializer."""
    tags = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Article
        fields = ['title', 'slug', 'summary', 'content', 'cover_image',
                  'category_id', 'tags', 'status', 'is_featured', 'is_top',
                  'allow_comment', 'source_type', 'source_url']

    category_id = serializers.IntegerField()

    def create(self, validated_data):
        from django.utils import timezone
        tags = validated_data.pop('tags', [])
        content = validated_data.get('content', '')
        validated_data['word_count'] = len(content)
        validated_data['reading_time'] = max(1, len(content) // 500)
        # Set published_at when status is Published
        if validated_data.get('status') == 1:
            validated_data['published_at'] = timezone.now()
        article = Article.objects.create(**validated_data)
        for tag_id in tags:
            ArticleTag.objects.create(article=article, tag_id=tag_id)
        return article

    def update(self, instance, validated_data):
        from django.utils import timezone
        tags = validated_data.pop('tags', None)
        content = validated_data.get('content', instance.content)
        validated_data['word_count'] = len(content)
        validated_data['reading_time'] = max(1, len(content) // 500)
        # Set published_at when transitioning to Published
        if validated_data.get('status') == 1 and not instance.published_at:
            validated_data['published_at'] = timezone.now()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.article_tags.all().delete()
            for tag_id in tags:
                ArticleTag.objects.create(article=instance, tag_id=tag_id)

        return instance


class ArchiveSerializer(serializers.Serializer):
    """Article archive serializer."""
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    count = serializers.IntegerField()
    articles = serializers.ListField()
