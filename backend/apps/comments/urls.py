from django.urls import path

from apps.comments.views import CommentViewSet

urlpatterns = [
    path('', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('<int:pk>/', CommentViewSet.as_view({'delete': 'destroy'}), name='comment-detail'),
    path('<int:pk>/review/', CommentViewSet.as_view({'patch': 'review'}), name='comment-review'),
]
