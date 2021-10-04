from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe

from .serializer_is_subscribed import IsSubscribedMixin

User = get_user_model()


class RecipeSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionsSerializer(
    serializers.ModelSerializer,
    IsSubscribedMixin,
):
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit is None:
            return
        recipes_limit = int(recipes_limit)
        serializers = RecipeSubscriptionsSerializer(
            obj.recipe.all()[:recipes_limit],
            many=True,
        )
        return serializers.data

    def get_recipes_count(self, obj):
        return obj.recipe.all().count()
