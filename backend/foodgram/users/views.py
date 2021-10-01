from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import serializers
from django.shortcuts import get_object_or_404
#from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.serializer import RecipeSerializer
from .serializer_user import MyUserSerializer
from .serializer import UserSubscriptionsSerializer
from .pagination import PaginationLimit

User = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PaginationLimit

    @action(['get'], detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        user = request.user
        user_sub = user.profile.subscriptions.all()
        page = self.paginate_queryset(user_sub)
        serializer = UserSubscriptionsSerializer(
            page, context=self.get_serializer_context(), many=True
        )
        page_serializer = self.get_paginated_response(serializer.data)
        x = page_serializer
        return page_serializer

    @action(['get', 'delete'], detail=True, url_path='subscribe')
    def subscribe(self, request, id=None, recipes_limit=3):
        user = request.user
        user_sub = get_object_or_404(User, pk=id)
        if request.method == 'DELETE':
            user.profile.subscriptions.remove(user_sub.pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        user.profile.subscriptions.add(user_sub.pk)
        serializer = UserSubscriptionsSerializer(
            user_sub, context=self.get_serializer_context(),# data = {'recipes_limit': recipes_limit},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
