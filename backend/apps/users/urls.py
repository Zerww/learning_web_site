from django.urls import path

from apps.users.views import AuthViewSet

urlpatterns = [
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='auth-login'),
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='auth-register'),
    path('refresh/', AuthViewSet.as_view({'post': 'refresh'}), name='auth-refresh'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='auth-logout'),
    path('me/', AuthViewSet.as_view({'get': 'me'}), name='auth-me'),
]
