from rest_framework import serializers

class IsSubscribedMixin(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            self.context['request'].user.is_authenticated
            and user.profile.subscriptions.all().filter(pk=obj.pk).exists()
        )
