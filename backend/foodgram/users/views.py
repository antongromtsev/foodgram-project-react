from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from .serializer import MyUserSerializer

User = get_user_model()


class MyUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = PageNumberPagination
    #permission_classes = [IsAdmin]
    #lookup_field = 'username'
    #filter_backends = [DjangoFilterBackend]
    #search_fields = ['user__username']

    @action(
        detail=False,
        methods=['GET'],
        #permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(
                self.get_serializer(request.user).data,
                status=status.HTTP_200_OK,
            )
