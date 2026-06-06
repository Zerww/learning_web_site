from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.comments.models import Comment
from apps.comments.serializers import (
    CommentCreateSerializer,
    CommentListSerializer,
    CommentReviewSerializer,
)
from utils.permissions import IsAdminUser, IsOwnerOrAdminForComment
from utils.response import created, error, success
from utils.throttling import CommentRateThrottle


class CommentViewSet(viewsets.ModelViewSet):
    """Comment CRUD endpoints."""
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content_type', 'object_id', 'status']
    ordering_fields = ['created_at', 'like_count']
    ordering = ['-created_at']

    def get_throttles(self):
        if self.action == 'create':
            return [CommentRateThrottle()]
        return super().get_throttles()

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [AllowAny()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsOwnerOrAdminForComment()]
        elif self.action == 'review':
            return [IsAdminUser()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action == 'review':
            return CommentReviewSerializer
        return CommentListSerializer

    def get_queryset(self):
        qs = Comment.objects.select_related('user', 'parent', 'reply_to_user')
        qs = qs.prefetch_related('replies__user', 'replies__reply_to_user')

        user = self.request.user
        if not user.is_authenticated or user.role != 1:
            qs = qs.filter(status=1)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # Only return top-level comments by default
        parent_id = request.query_params.get('parent_id')
        if parent_id is None:
            queryset = queryset.filter(parent=None)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success({'list': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error('评论提交失败', code=400, errors=serializer.errors)

        data = serializer.validated_data
        user = request.user if request.user.is_authenticated else None

        comment = Comment.objects.create(
            content=data['content'],
            content_type=data['content_type'],
            object_id=data['object_id'],
            user=user if user else None,
            nickname=data.get('nickname') if not user else None,
            email=data.get('email') if not user else None,
            website=data.get('website'),
            parent_id=data.get('parent_id'),
            reply_to_user_id=data.get('reply_to_user_id'),
            ip_address=request.META.get('REMOTE_ADDR'),
        )

        return created({
            'id': comment.id,
            'content': comment.content,
            'status': comment.status,
        }, message='评论已提交，等待审核')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        instance.delete()
        return success(message='删除成功')

    @action(detail=True, methods=['patch'])
    def review(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error('审核失败', code=400, errors=serializer.errors)
        instance.status = serializer.validated_data['status']
        instance.save(update_fields=['status'])
        status_map = {1: '已通过', 2: '已拒绝'}
        return success(message=f'审核{status_map.get(instance.status, "完成")}')
