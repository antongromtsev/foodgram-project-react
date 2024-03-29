from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.pagination import PaginationLimit
from recipes.serializer import UserSubscriptionsSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.models import Subscription

User = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PaginationLimit

    @action(['get'], detail=False, url_path='subscriptions')
    def subscriptions(self, request):
        user_sub = User.objects.filter(followed__user=request.user)
        page = self.paginate_queryset(user_sub)
        serializer = UserSubscriptionsSerializer(
            page, context=self.get_serializer_context(), many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(['get', 'delete'], detail=True, url_path='subscribe')
    def subscribe(self, request, id=None):
        user = request.user
        user_sub = get_object_or_404(User, pk=id)
        if user == user_sub:
            return Response(
                "You can't subscribe to yourself",
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            Subscription.objects.filter(user=user.pk, user_sub=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Subscription.objects.get_or_create(user=user, user_sub=user_sub)
        serializer = UserSubscriptionsSerializer(
            user_sub, context=self.get_serializer_context(),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
