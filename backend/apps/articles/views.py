from datetime import datetime

from django.db import models
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.articles.models import Article
from apps.articles.serializers import (
    ArchiveSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
)
from utils.permissions import IsAdminUser
from utils.response import created, error, success


class ArticleViewSet(viewsets.ModelViewSet):
    """Article CRUD endpoints."""
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category_id': ['exact'],
        'status': ['exact'],
        'is_featured': ['exact'],
        'is_top': ['exact'],
    }
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['created_at', 'published_at', 'view_count', 'like_count']
    ordering = ['-is_top', '-published_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'archive']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateSerializer
        return ArticleListSerializer

    def get_queryset(self):
        qs = Article.objects.select_related('category', 'author').prefetch_related('tags')
        if self.action == 'list':
            if not self.request.user.is_authenticated or self.request.user.role != 1:
                qs = qs.filter(status=1)
            # Manual year/month filtering (not supported by filterset_fields)
            year = self.request.query_params.get('year')
            month = self.request.query_params.get('month')
            if year:
                qs = qs.filter(published_at__year=year)
            if month:
                qs = qs.filter(published_at__month=month)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        Article.objects.filter(id=instance.id).update(view_count=models.F('view_count') + 1)
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

    @action(detail=False, methods=['get'])
    def archive(self, request):
        """Get article archive grouped by year and month."""
        articles = Article.objects.filter(status=1, published_at__isnull=False)

        # Truncate published_at to year/month using TruncMonth
        from django.db.models.functions import TruncMonth
        date_counts = (
            articles
            .annotate(month=TruncMonth('published_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('-month')
        )

        archives = []
        for entry in date_counts:
            m = entry['month']
            if not m:
                continue
            year = m.year
            month = m.month
            month_articles = list(
                articles.filter(
                    published_at__year=year,
                    published_at__month=month
                ).values('id', 'title', 'published_at')[:10]
            )
            archives.append({
                'year': year,
                'month': month,
                'count': entry['count'],
                'articles': month_articles,
            })

        return success({'archives': archives})
