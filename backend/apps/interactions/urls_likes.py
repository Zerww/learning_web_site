from django.urls import path

from apps.interactions.views import LikeViewSet

urlpatterns = [
    path('status/', LikeViewSet.as_view({'get': 'status'}), name='like-status'),
    path('my/', LikeViewSet.as_view({'get': 'my_likes'}), name='like-my'),
    path('', LikeViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='like-list'),
]
