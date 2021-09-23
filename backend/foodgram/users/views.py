from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from .serializer import MyUserSerializer

User = get_user_model()


class MyUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    #permission_classes = [IsAdmin]
    #lookup_field = 'username'
    #filter_backends = [DjangoFilterBackend]
    #search_fields = ['user__username']