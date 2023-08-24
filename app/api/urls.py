"""
API url configuration.
"""
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.urls import path, include


app_name = 'api'  # used for reverse mapping

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:api-schema'), name='api-docs'),
    path('user/', include('user.urls')),
]