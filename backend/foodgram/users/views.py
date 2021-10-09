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
        queryset = User.objects.filter(following__user_sub=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSubscriptionsSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserSubscriptionsSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

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
