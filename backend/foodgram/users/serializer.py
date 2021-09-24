from rest_framework import serializers
from django.contrib.auth import get_user_model


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
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
