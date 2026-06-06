from rest_framework import serializers

from apps.settings.models import Setting


class SettingPublicSerializer(serializers.ModelSerializer):
    """Public settings serializer (read-only)."""

    class Meta:
        model = Setting
        fields = ['key', 'value']


class SettingSerializer(serializers.ModelSerializer):
    """Admin settings serializer."""

    class Meta:
        model = Setting
        fields = ['id', 'key', 'value', 'description', 'is_public']
        read_only_fields = ['id']
