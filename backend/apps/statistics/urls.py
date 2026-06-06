from django.urls import path

from apps.statistics.views import StatisticsViewSet

urlpatterns = [
    path('', StatisticsViewSet.as_view({'get': 'list'}), name='statistics'),
    path('visits/', StatisticsViewSet.as_view({'get': 'list'}), name='visit-logs'),
]
