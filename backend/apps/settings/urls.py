from django.urls import path

from apps.settings.views import SettingViewSet

urlpatterns = [
    path('public/', SettingViewSet.as_view({'get': 'public'}), name='settings-public'),
    path('', SettingViewSet.as_view({'get': 'list'}), name='settings-list'),
    path('<str:pk>/', SettingViewSet.as_view({'put': 'update'}), name='settings-update'),
]
