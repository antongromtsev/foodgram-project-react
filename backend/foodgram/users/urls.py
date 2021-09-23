from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyUserViewSet


router = DefaultRouter()
router.register('users', MyUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/', include(auth_paths))
]