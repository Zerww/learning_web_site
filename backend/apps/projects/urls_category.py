from django.urls import path

from apps.projects.views import CategoryViewSet

urlpatterns = [
    path('', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('<int:pk>/', CategoryViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='category-detail'),
]
