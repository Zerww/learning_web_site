from django.urls import path

from apps.projects.views import TagViewSet

urlpatterns = [
    path('', TagViewSet.as_view({'get': 'list', 'post': 'create'}), name='tag-list'),
    path('<int:pk>/', TagViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='tag-detail'),
]
