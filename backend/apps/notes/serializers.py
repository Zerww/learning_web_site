from rest_framework import serializers

from apps.notes.models import Note, NoteTag
from apps.projects.serializers import CategorySerializer, TagSerializer


class NoteListSerializer(serializers.ModelSerializer):
    """Note list serializer."""
    category = CategorySerializer(read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'slug', 'category', 'learning_stage',
                  'progress', 'difficulty', 'status', 'view_count',
                  'like_count', 'children_count', 'created_at']

    def get_children_count(self, obj):
        return obj.children.filter(status=1).count()


class NoteDetailSerializer(serializers.ModelSerializer):
    """Note detail serializer."""
    category = CategorySerializer(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = '__all__'

    def get_children(self, obj):
        children = obj.children.filter(status=1).order_by('sort_order')
        return [{'id': c.id, 'title': c.title, 'progress': c.progress} for c in children]


class NoteCreateSerializer(serializers.ModelSerializer):
    """Note create/update serializer."""
    tags = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Note
        fields = ['title', 'slug', 'content', 'category_id', 'learning_stage',
                  'progress', 'difficulty', 'parent_id', 'sort_order', 'status', 'tags']

    category_id = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        note = Note.objects.create(**validated_data)
        for tag_id in tags:
            NoteTag.objects.create(note=note, tag_id=tag_id)
        return note


class NoteProgressSerializer(serializers.Serializer):
    """Note progress update serializer."""
    progress = serializers.IntegerField(min_value=0, max_value=100)
