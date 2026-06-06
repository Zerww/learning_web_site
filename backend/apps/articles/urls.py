from django.urls import path

from apps.articles.views import ArticleViewSet

urlpatterns = [
    path('archive/', ArticleViewSet.as_view({'get': 'archive'}), name='article-archive'),
    path('', ArticleViewSet.as_view({'get': 'list', 'post': 'create'}), name='article-list'),
    path('<int:pk>/', ArticleViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='article-detail'),
]
