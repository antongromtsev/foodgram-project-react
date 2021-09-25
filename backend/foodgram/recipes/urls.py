from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, RecipeViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/', include(auth_paths))
]