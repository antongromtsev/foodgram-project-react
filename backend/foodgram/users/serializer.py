from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.conf import settings


User = get_user_model()


class MyUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            self.context['request'].user.is_authenticated
            and user.profile.subscriptions.all().filter(pk=obj.pk).exists()
        )

    class Meta:
        model = User
        fields = (
            (settings.LOGIN_FIELD, )
            + tuple(User.REQUIRED_FIELDS)
            + ('is_subscribed',)
        )
        read_only_fields = (settings.LOGIN_FIELD,)
