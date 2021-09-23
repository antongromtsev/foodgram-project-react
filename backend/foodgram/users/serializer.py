from rest_framework import serializers
from django.contrib.auth import get_user_model

#from recipes.models import ProfileUser


User = get_user_model()


class MyUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        x = self.context['request'].user
        x = x.profile.all()
        return x.filter(pk=obj.pk).exists()

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