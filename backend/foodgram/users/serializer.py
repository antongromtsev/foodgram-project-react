from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.conf import settings

from recipes.serializer import RecipeSerializer
from recipes.models import Recipe
from users.serializer_user import MyUserSerializer
from .serializer_is_subscribed import IsSubscribedMixin

User =get_user_model()

class RecipeSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class UserSubscriptionsSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        y = obj.profile.favourites.all()
        serializers = RecipeSubscriptionsSerializer(obj.profile.favourites.all(), many=True)
        x = serializers.data
        return serializers.data
    
    def get_recipes_count(self, obj):
        return obj.profile.subscriptions.all().count()
    
    # def to_representation(self, instance):
    #     x = instance
    #     return {
    #         'score': instance,
    #         'player_name': instance
    #     }

    def save(self, **kwargs):
        return super().save(**kwargs)