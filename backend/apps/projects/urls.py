from django.urls import path

from apps.projects.views import ProjectViewSet

urlpatterns = [
    path('', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list'),
    path('<int:pk>/', ProjectViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='project-detail'),
]
