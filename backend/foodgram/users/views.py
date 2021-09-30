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
    # pagination_class = PageNumberPagination

    @action(["get"], detail=False, url_path="subscriptions")
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        user_serializer = MyUserSerializer(user)
        # user_serializer.is_valid
        #user = user_serializer.data
        #recipe = user.profile.subscriptions.all()
        # recipe_serializer = RecipeSerializer(recipe, many=True)
        serializer = UserSubscriptionsSerializer(
            user, context=self.get_serializer_context()
        )
        serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)