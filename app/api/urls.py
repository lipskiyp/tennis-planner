"""
API url configuration.
"""
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('courts', views.CourtViewSet)  # creates new endpoint, i.e. /api/recipes/, and assigns all views from RecipeViewSet to the viewset
router.register('sessions', views.TrainingSessionViewSet)


app_name = 'api'  # used for reverse mapping

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:api-schema'), name='api-docs'),
    path('user/', include('user.urls')),
    path('', include(router.urls)),
]