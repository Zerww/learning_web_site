from rest_framework import serializers


class LikeSerializer(serializers.Serializer):
    """Like action serializer."""
    content_type = serializers.ChoiceField(choices=[1, 2, 3, 4], label='内容类型')
    object_id = serializers.IntegerField(label='对象ID')


class FavoriteSerializer(serializers.Serializer):
    """Favorite action serializer."""
    content_type = serializers.ChoiceField(choices=[1, 2, 3], label='收藏对象类型')
    object_id = serializers.IntegerField(label='收藏对象ID')
    folder_name = serializers.CharField(required=False, allow_null=True, max_length=50,
                                        label='收藏夹名称')
