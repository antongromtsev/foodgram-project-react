from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.conf import settings

from .serializer_is_subscribed import IsSubscribedMixin

User = get_user_model()


class MyUserSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    
    class Meta:
        model = User
        fields = (
            (settings.LOGIN_FIELD, )
            + tuple(User.REQUIRED_FIELDS)
            + ('is_subscribed',)
        )
        read_only_fields = (settings.LOGIN_FIELD,)




