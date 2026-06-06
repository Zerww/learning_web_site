from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.projects.models import Category, Project, Tag
from apps.projects.serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    TagCreateSerializer,
    TagSerializer,
)
from utils.permissions import IsAdminUser
from utils.response import created, error, success


class ProjectViewSet(viewsets.ModelViewSet):
    """Project CRUD endpoints."""
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category_id': ['exact'],
        'status': ['exact'],
        'is_featured': ['exact'],
        'difficulty': ['exact'],
    }
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'published_at', 'view_count', 'like_count']
    ordering = ['-published_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action == 'retrieve':
            return ProjectDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateSerializer
        return ProjectListSerializer

    def get_queryset(self):
        qs = Project.objects.select_related('category', 'author').prefetch_related('tags')
        if self.action == 'list':
            if not self.request.user.is_authenticated or self.request.user.role != 1:
                qs = qs.filter(status=1)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Increment view count
        Project.objects.filter(id=instance.id).update(view_count=models.F('view_count') + 1)
        return success(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Filter by tags
        tags_param = request.query_params.get('tags')
        if tags_param:
            tag_ids = [int(t) for t in tags_param.split(',') if t.isdigit()]
            for tid in tag_ids:
                queryset = queryset.filter(tags__id=tid)

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
        return success({
            'id': instance.id,
            'title': instance.title,
            'slug': instance.slug,
        }, message='更新成功')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success(message='删除成功')


class CategoryViewSet(viewsets.ModelViewSet):
    """Category CRUD endpoints."""
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'parent_id']
    ordering = ['sort_order', 'id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateSerializer
        return CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success({'list': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error('创建失败', code=400, errors=serializer.errors)
        serializer.save()
        return created({'id': serializer.instance.id, 'name': serializer.instance.name}, message='创建成功')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error('更新失败', code=400, errors=serializer.errors)
        serializer.save()
        return success(message='更新成功')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success(message='删除成功')


class TagViewSet(viewsets.ModelViewSet):
    """Tag CRUD endpoints."""
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type']
    ordering_fields = ['usage_count', 'name']
    ordering = ['-usage_count']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TagCreateSerializer
        return TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success({'list': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error('创建失败', code=400, errors=serializer.errors)
        serializer.save()
        return created({'id': serializer.instance.id, 'name': serializer.instance.name}, message='创建成功')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error('更新失败', code=400, errors=serializer.errors)
        serializer.save()
        return success(message='更新成功')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success(message='删除成功')
