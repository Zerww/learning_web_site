"""Main URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/users/', include('apps.users.urls_profile')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/articles/', include('apps.articles.urls')),
    path('api/v1/notes/', include('apps.notes.urls')),
    path('api/v1/categories/', include('apps.projects.urls_category')),
    path('api/v1/tags/', include('apps.projects.urls_tag')),
    path('api/v1/comments/', include('apps.comments.urls')),
    path('api/v1/likes/', include('apps.interactions.urls_likes')),
    path('api/v1/favorites/', include('apps.interactions.urls_favorites')),
    path('api/v1/search/', include('apps.articles.urls_search')),
    path('api/v1/home/', include('apps.statistics.urls_home')),
    path('api/v1/statistics/', include('apps.statistics.urls')),
    path('api/v1/settings/', include('apps.settings.urls')),
    path('api/v1/upload/', include('apps.statistics.urls_upload')),

    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
