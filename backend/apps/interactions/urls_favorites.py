from django.urls import path

from apps.interactions.views import FavoriteViewSet

urlpatterns = [
    path('', FavoriteViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='favorite-list'),
]
