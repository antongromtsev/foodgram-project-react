from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from djoser.views import UserViewSet

from .serializer import MyUserSerializer 

User = get_user_model()


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = PageNumberPagination

