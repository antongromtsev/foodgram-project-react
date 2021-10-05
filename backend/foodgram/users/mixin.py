from rest_framework import serializers

from .profile import Subscription


class IsSubscribedMixin(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and Subscription.objects.filter(
                follower=user.pk, followed=obj.pk).exists()
        )
