from rest_framework import serializers

from apps.comments.models import Comment


class ReplySerializer(serializers.ModelSerializer):
    """Reply sub-serializer."""
    user = serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'reply_to', 'like_count', 'status', 'created_at']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'nickname': obj.user.nickname or obj.user.username,
            'avatar': obj.user.avatar,
        }

    def get_reply_to(self, obj):
        if obj.reply_to_user:
            return {
                'id': obj.reply_to_user.id,
                'nickname': obj.reply_to_user.nickname or obj.reply_to_user.username,
            }
        return None


class CommentListSerializer(serializers.ModelSerializer):
    """Comment list serializer with replies."""
    user = serializers.SerializerMethodField()
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'content_type', 'object_id', 'user',
                  'parent', 'replies', 'like_count', 'status', 'created_at']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'nickname': obj.user.nickname or obj.user.username,
            'avatar': obj.user.avatar,
        }


class CommentCreateSerializer(serializers.ModelSerializer):
    """Comment creation serializer."""

    class Meta:
        model = Comment
        fields = ['content', 'content_type', 'object_id', 'parent_id',
                  'reply_to_user_id', 'nickname', 'email', 'website']

    content_type = serializers.IntegerField()
    object_id = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    reply_to_user_id = serializers.IntegerField(required=False, allow_null=True)
    nickname = serializers.CharField(required=False, allow_null=True, max_length=50)
    email = serializers.EmailField(required=False, allow_null=True)
    website = serializers.URLField(required=False, allow_null=True, max_length=255)

    def validate(self, data):
        user = self.context.get('request').user
        if not user.is_authenticated:
            if not data.get('nickname'):
                raise serializers.ValidationError('访客请填写昵称')
            if not data.get('email'):
                raise serializers.ValidationError('访客请填写邮箱')
        return data


class CommentReviewSerializer(serializers.Serializer):
    """Comment review (admin) serializer."""
    status = serializers.ChoiceField(choices=[1, 2], label='审核状态')
