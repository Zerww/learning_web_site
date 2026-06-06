from django.urls import path

from apps.users.views import ProfileViewSet, UserViewSet

urlpatterns = [
    path('profile/', ProfileViewSet.as_view({'put': 'profile'}), name='user-profile'),
    path('change-password/', ProfileViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),
]
