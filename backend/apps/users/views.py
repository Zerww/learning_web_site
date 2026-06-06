from django.contrib.auth import update_session_auth_hash
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserProfileSerializer,
    UserPublicSerializer,
)
from utils.permissions import IsAdminUser
from utils.response import created, error, success
from utils.throttling import LoginRateThrottle


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints."""

    def get_permissions(self):
        if self.action in ['login', 'register']:
            return [AllowAny()]
        elif self.action in ['me']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=False, methods=['post'], throttle_classes=[LoginRateThrottle])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error('用户名或密码错误', code=400, errors=serializer.errors)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user.last_login_at = None  # Will be set by signal
        user.save(update_fields=['last_login_at'])
        return success({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'expires_in': 7200,
            'user': {
                'id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'role': user.role,
            },
        }, message='登录成功')

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error('注册失败', code=400, errors=serializer.errors)
        user = serializer.save()
        return created({
            'user_id': user.id,
            'username': user.username,
        }, message='注册成功')

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return error('refresh_token不能为空', code=400)
        try:
            token = RefreshToken(refresh_token)
            return success({
                'access_token': str(token.access_token),
                'expires_in': 7200,
            }, message='刷新成功')
        except Exception:
            return error('Token无效或已过期', code=401)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return success(message='注销成功')

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return success(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User profile endpoints."""

    def get_serializer_class(self):
        if self.action == 'list' and self.request.user.role == 1:
            return UserListSerializer
        return UserPublicSerializer

    def get_queryset(self):
        return User.objects.filter(status=1)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserPublicSerializer(instance)
        return success(serializer.data)


class ProfileViewSet(viewsets.ViewSet):
    """Profile management endpoints."""

    @action(detail=False, methods=['put'])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return error('更新失败', code=400, errors=serializer.errors)
        serializer.save()
        return success({'id': request.user.id, 'nickname': request.user.nickname}, message='更新成功')

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error('密码修改失败', code=400, errors=serializer.errors)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return error('旧密码不正确', code=400)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
        return success(message='密码修改成功')
