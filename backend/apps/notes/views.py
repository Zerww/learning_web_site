from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.notes.models import Note
from apps.notes.serializers import (
    NoteCreateSerializer,
    NoteDetailSerializer,
    NoteListSerializer,
    NoteProgressSerializer,
)
from utils.permissions import IsAdminUser
from utils.response import created, error, success


class NoteViewSet(viewsets.ModelViewSet):
    """Note CRUD endpoints."""
    queryset = Note.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category_id': ['exact'],
        'learning_stage': ['exact'],
        'parent_id': ['exact', 'isnull'],
        'status': ['exact'],
    }
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'sort_order', 'view_count', 'like_count']
    ordering = ['-sort_order', '-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'list':
            return NoteListSerializer
        elif self.action == 'retrieve':
            return NoteDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return NoteCreateSerializer
        return NoteListSerializer

    def get_queryset(self):
        qs = Note.objects.select_related('category', 'author').prefetch_related('children')
        if self.action == 'list':
            if not self.request.user.is_authenticated or self.request.user.role != 1:
                qs = qs.filter(status=1)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success({'list': serializer.data})

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error('创建失败', code=400, errors=serializer.errors)
        self.perform_create(serializer)
        return created({
            'id': serializer.instance.id,
            'title': serializer.instance.title,
            'slug': serializer.instance.slug,
        }, message='创建成功')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error('更新失败', code=400, errors=serializer.errors)
        self.perform_update(serializer)
        return success(message='更新成功')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success(message='删除成功')

    @action(detail=True, methods=['patch'])
    def progress(self, request, pk=None):
        instance = self.get_object()
        serializer = NoteProgressSerializer(data=request.data)
        if not serializer.is_valid():
            return error('更新失败', code=400, errors=serializer.errors)
        instance.progress = serializer.validated_data['progress']
        instance.save(update_fields=['progress'])
        return success({'id': instance.id, 'progress': instance.progress}, message='更新成功')
