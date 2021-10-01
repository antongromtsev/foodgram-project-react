from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import serializers
#from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.serializer import RecipeSerializer
from .serializer_user import MyUserSerializer
from .serializer import UserSubscriptionsSerializer

User = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    @action(["get"], detail=False, url_path="subscriptions")
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        user_sub = user.profile.subscriptions.all()
        user_serializer = MyUserSerializer(user)
        page = self.paginate_queryset(user_sub)
        serializer = UserSubscriptionsSerializer(
            page, context=self.get_serializer_context(), many=True
        )
        page_serializer = self.get_paginated_response(serializer.data)
        x = page_serializer
        return page_serializer
