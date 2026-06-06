from django.urls import path

from apps.notes.views import NoteViewSet

urlpatterns = [
    path('', NoteViewSet.as_view({'get': 'list', 'post': 'create'}), name='note-list'),
    path('<int:pk>/', NoteViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
    }), name='note-detail'),
    path('<int:pk>/progress/', NoteViewSet.as_view({'patch': 'progress'}), name='note-progress'),
]
