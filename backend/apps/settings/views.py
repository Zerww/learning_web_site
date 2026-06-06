from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.settings.models import Setting
from apps.settings.serializers import SettingPublicSerializer, SettingSerializer
from utils.permissions import IsAdminUser
from utils.response import error, success


class SettingViewSet(viewsets.ViewSet):
    """System settings endpoints."""

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        settings = Setting.objects.filter(is_public=True)
        serializer = SettingPublicSerializer(settings, many=True)
        data = {item['key']: item['value'] for item in serializer.data}
        return success(data)

    def list(self, request):
        if not request.user.is_authenticated or request.user.role != 1:
            return error('无权限访问', code=403)
        settings = Setting.objects.all()
        serializer = SettingSerializer(settings, many=True)
        return success({'list': serializer.data})

    def update(self, request, pk=None):
        if not request.user.is_authenticated or request.user.role != 1:
            return error('无权限访问', code=403)
        try:
            setting = Setting.objects.get(key=pk)
        except Setting.DoesNotExist:
            setting = Setting(key=pk)

        setting.value = request.data.get('value', setting.value)
        if 'description' in request.data:
            setting.description = request.data['description']
        if 'is_public' in request.data:
            setting.is_public = request.data['is_public']
        setting.save()

        return success(message='配置更新成功')
