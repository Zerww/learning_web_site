from django.urls import path
from rest_framework.decorators import api_view

from apps.articles.models import Article
from apps.notes.models import Note
from apps.projects.models import Project
from utils.response import error, success


@api_view(['GET'])
def search(request):
    """Full-text search across articles, projects, and notes."""
    keyword = request.query_params.get('keyword', '').strip()
    search_type = request.query_params.get('type', 'all')

    if not keyword:
        return error('请输入搜索关键词', code=400)

    results = {}
    total = 0

    if search_type in ('all', 'article'):
        articles = Article.objects.filter(
            status=1, title__icontains=keyword
        ).values('id', 'title', 'summary')[:10]
        results['articles'] = {'count': articles.count(), 'list': list(articles)}
        total += articles.count()

    if search_type in ('all', 'project'):
        projects = Project.objects.filter(
            status=1, title__icontains=keyword
        ).values('id', 'title', 'description')[:10]
        results['projects'] = {'count': projects.count(), 'list': list(projects)}
        total += projects.count()

    if search_type in ('all', 'note'):
        notes = Note.objects.filter(
            status=1, title__icontains=keyword
        ).values('id', 'title')[:10]
        results['notes'] = {'count': notes.count(), 'list': list(notes)}
        total += notes.count()

    return success({
        'keyword': keyword,
        'results': results,
        'total': total,
    })


urlpatterns = [
    path('', search, name='search'),
]
