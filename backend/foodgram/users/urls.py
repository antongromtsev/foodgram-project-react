from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyUserViewSet

router = DefaultRouter()
router.register(r'users', MyUserViewSet, basename='MyUserViewSet')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
