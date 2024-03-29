from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class IsSubscribedMixin(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and Subscription.objects.filter(
                user=user.pk, user_sub=obj.pk).exists()
        )


class MyUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )
    first_name = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(
                150,
                message='Ensure first_name has at most 150 characters.'
            )
        ]
    )
    last_name = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(
                150,
                message='Ensure last_name has at most 150 characters.'
            )
        ]
    )
    password = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(
                150,
                message='Ensure last_name has at most 150 characters.'
            )
        ]
    )

    class Meta:
        model = User

        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'password',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        serializers = UserRepresentationSerializer(
            instance, context=self.context
        )
        return serializers.data


class UserRepresentationSerializer(serializers.ModelSerializer,
                                   IsSubscribedMixin):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed',
        )
