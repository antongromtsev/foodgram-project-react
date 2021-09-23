from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/', include(auth_paths))
]