from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.articles.models import Article
from apps.comments.models import Comment
from apps.interactions.models import Favorite, Like
from apps.projects.models import Project, Tag
from apps.statistics.models import VisitLog
from utils.permissions import IsAdminUser
from utils.response import error, success


class HomeViewSet(viewsets.ViewSet):
    """Home page data endpoint."""
    permission_classes = [AllowAny]

    def list(self, request):
        profile_data = {
            'nickname': '管理员',
            'avatar': None,
            'bio': '个人简介',
            'skills': ['Vue', 'Django', 'MySQL', 'Python', 'TypeScript'],
            'github_url': None,
            'social_links': {
                'github': None,
                'email': None,
            },
        }

        article_count = Article.objects.filter(status=1).count()
        project_count = Project.objects.filter(status=1).count()

        total_views = (
            Article.objects.filter(status=1).aggregate(s=Sum('view_count'))['s'] or 0
        )
        total_likes = (
            Article.objects.filter(status=1).aggregate(s=Sum('like_count'))['s'] or 0
        )

        stats = {
            'article_count': article_count,
            'project_count': project_count,
            'total_views': total_views,
            'total_likes': total_likes,
        }

        featured_projects = Project.objects.filter(status=1, is_featured=True)[:6]
        featured_articles = Article.objects.filter(status=1, is_featured=True)[:6]
        latest_articles = Article.objects.filter(status=1).order_by('-published_at')[:6]
        popular_tags = Tag.objects.all().order_by('-usage_count')[:20]

        return success({
            'profile': profile_data,
            'statistics': stats,
            'featured_projects': [
                {'id': p.id, 'title': p.title, 'cover_image': p.cover_image, 'slug': p.slug}
                for p in featured_projects
            ],
            'featured_articles': [
                {'id': a.id, 'title': a.title, 'summary': a.summary, 'slug': a.slug}
                for a in featured_articles
            ],
            'latest_articles': [
                {'id': a.id, 'title': a.title, 'slug': a.slug, 'published_at': a.published_at}
                for a in latest_articles
            ],
            'popular_tags': [
                {'id': t.id, 'name': t.name, 'usage_count': t.usage_count}
                for t in popular_tags
            ],
        })


class StatisticsViewSet(viewsets.ViewSet):
    """Statistics endpoints (admin only)."""
    permission_classes = [IsAdminUser]

    def list(self, request):
        stat_type = request.query_params.get('type', 'overview')

        if stat_type == 'overview':
            return self._overview(request)
        elif stat_type == 'visit':
            return self._visit_stats(request)
        elif stat_type == 'content':
            return self._content_stats(request)
        return error('无效的统计类型', code=400)

    def _overview(self, request):
        total_views = (
            Article.objects.aggregate(s=Sum('view_count'))['s'] or 0
        ) + (Project.objects.aggregate(s=Sum('view_count'))['s'] or 0)
        total_likes = Like.objects.count()
        total_comments = Comment.objects.count()
        total_favorites = Favorite.objects.count()

        return success({
            'overview': {
                'total_views': total_views,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'total_favorites': total_favorites,
                'articles_count': Article.objects.count(),
                'projects_count': Project.objects.count(),
            },
            'trend': {
                'views_trend': list(
                    VisitLog.objects
                    .annotate(date=TruncDate('created_at'))
                    .values('date')
                    .annotate(count=Count('id'))
                    .order_by('date')[:30]
                ),
            },
        })

    def _visit_stats(self, request):
        qs = VisitLog.objects.all()
        if request.query_params.get('start_date'):
            qs = qs.filter(created_at__gte=request.query_params['start_date'])
        if request.query_params.get('end_date'):
            qs = qs.filter(created_at__lte=request.query_params['end_date'])
        if request.query_params.get('content_type'):
            qs = qs.filter(content_type=request.query_params['content_type'])
        if request.query_params.get('object_id'):
            qs = qs.filter(object_id=request.query_params['object_id'])

        page = self.paginate_queryset(qs)
        if page is not None:
            data = list(page.values())
            return self.get_paginated_response(data)

        return success({'list': list(qs.values()[:100])})

    def _content_stats(self, request):
        top_articles = Article.objects.filter(status=1).order_by('-view_count')[:10]
        top_projects = Project.objects.filter(status=1).order_by('-view_count')[:10]

        return success({
            'top_articles': [
                {'id': a.id, 'title': a.title, 'view_count': a.view_count}
                for a in top_articles
            ],
            'top_projects': [
                {'id': p.id, 'title': p.title, 'view_count': p.view_count}
                for p in top_projects
            ],
        })


class UploadViewSet(viewsets.ViewSet):
    """File upload endpoint."""
    permission_classes = [IsAdminUser]

    def create(self, request):
        file = request.FILES.get('file')
        if not file:
            return error('请选择要上传的文件', code=400)

        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            return error('不支持的文件类型', code=400)

        if file.size > 5 * 1024 * 1024:
            return error('文件大小不能超过5MB', code=400)

        from django.core.files.storage import default_storage
        from django.utils import timezone

        now = timezone.now()
        path = default_storage.save(
            f'uploads/{now.year}/{now.month:02d}/{file.name}',
            file
        )
        url = default_storage.url(path)

        return success({
            'url': url,
            'filename': file.name,
            'size': file.size,
        }, message='上传成功')
