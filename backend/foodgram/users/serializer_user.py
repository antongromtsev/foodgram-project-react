from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers

from .serializer_is_subscribed import IsSubscribedMixin

User = get_user_model()


class MyUserSerializer(serializers.ModelSerializer, IsSubscribedMixin):

    class Meta:
        model = User
        fields = (
            (settings.LOGIN_FIELD, )
            + ('id', )
            + tuple(User.REQUIRED_FIELDS)
            + ('is_subscribed',)
        )
        read_only_fields = (settings.LOGIN_FIELD,)
