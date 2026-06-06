from django.urls import path

from apps.statistics.views import HomeViewSet

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),
]
