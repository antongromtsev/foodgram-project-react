from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Tag, Recipe, Ingredient, IngredientValue
from users.serializer import MyUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientValueSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = IngredientValue
        fields = (
            'ingredient',
        )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = representation['ingredient']
        representation['amount'] = instance.amount

        return representation

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeSerializer(serializers.ModelSerializer):
    
    tags = TagSerializer(many=True)
    author = MyUserSerializer()

    ingredients = IngredientValueSerializer(source='ingredientvalue_set', many=True)
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.profile.favourites.all().filter(pk=obj.pk).exists()

    def get_is_in_shopping_cart(self, obj):
        user =self.context['request'].user 
        return user.profile.shopping_list.all().filter(pk=obj.pk).exists()


    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
