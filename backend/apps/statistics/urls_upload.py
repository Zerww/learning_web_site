from django.urls import path

from apps.statistics.views import UploadViewSet

urlpatterns = [
    path('image/', UploadViewSet.as_view({'post': 'create'}), name='upload-image'),
]
