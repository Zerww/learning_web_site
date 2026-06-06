from rest_framework import serializers

from apps.projects.models import Category, Project, ProjectTag, Tag


class TagSerializer(serializers.ModelSerializer):
    """Tag list serializer."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color', 'type', 'usage_count']


class TagCreateSerializer(serializers.ModelSerializer):
    """Tag create/update serializer."""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color', 'type']


class CategorySerializer(serializers.ModelSerializer):
    """Category list serializer with children."""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'type', 'icon',
                  'sort_order', 'parent', 'children', 'count']

    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return CategorySerializer(children, many=True).data
        return []

    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        type_map = {1: 'projects', 2: 'articles', 3: 'notes'}
        related_name = type_map.get(obj.type)
        if related_name:
            return getattr(obj, related_name).filter(status=1).count()
        return 0


class CategoryCreateSerializer(serializers.ModelSerializer):
    """Category create/update serializer."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'type', 'parent_id', 'sort_order', 'icon']

    parent_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        parent_id = validated_data.pop('parent_id', None)
        if parent_id:
            validated_data['parent'] = Category.objects.get(id=parent_id)
        return super().create(validated_data)


class ProjectListSerializer(serializers.ModelSerializer):
    """Project list serializer."""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tech_stack = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'cover_image', 'category',
                  'tags', 'tech_stack', 'github_url', 'demo_url', 'status',
                  'is_featured', 'view_count', 'like_count', 'favorite_count',
                  'difficulty', 'published_at', 'author']

    def get_tech_stack(self, obj):
        return obj.tech_stack.split(',') if obj.tech_stack else []

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'nickname': obj.author.nickname or obj.author.username,
            'avatar': obj.author.avatar,
        }


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Project detail serializer."""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tech_stack = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    related_projects = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_tech_stack(self, obj):
        return obj.tech_stack.split(',') if obj.tech_stack else []

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'nickname': obj.author.nickname or obj.author.username,
            'avatar': obj.author.avatar,
        }

    def get_related_projects(self, obj):
        related = Project.objects.filter(
            category=obj.category, status=1
        ).exclude(id=obj.id)[:4]
        return [{'id': p.id, 'title': p.title, 'cover_image': p.cover_image} for p in related]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Like
            return Like.objects.filter(content_type=2, object_id=obj.id, user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Favorite
            return Favorite.objects.filter(content_type=2, object_id=obj.id, user=request.user).exists()
        return False


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Project create/update serializer."""
    tags = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Project
        fields = ['title', 'slug', 'description', 'content', 'cover_image',
                  'category_id', 'tags', 'tech_stack', 'github_url', 'demo_url',
                  'video_url', 'status', 'is_featured', 'difficulty',
                  'start_date', 'end_date']

    category_id = serializers.IntegerField()

    def create(self, validated_data):
        from django.utils import timezone
        tags = validated_data.pop('tags', [])
        tech_stack = validated_data.get('tech_stack')
        if isinstance(tech_stack, list):
            validated_data['tech_stack'] = ','.join(tech_stack)
        if validated_data.get('status') == 1:
            validated_data['published_at'] = timezone.now()
        project = Project.objects.create(**validated_data)
        for tag_id in tags:
            ProjectTag.objects.create(project=project, tag_id=tag_id)
        return project
