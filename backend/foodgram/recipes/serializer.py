# from django.db import models
# from django.db.models import fields
from rest_framework import fields, serializers
from drf_base64.fields import Base64ImageField
from django.shortcuts import get_object_or_404

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
    ingredients = IngredientValueSerializer(
        source='ingredientvalue_set',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField(
        'get_is_favorited',
        )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart',
    )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            user.profile.favourites.all().filter(pk=obj.pk).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            user.profile.shopping_list.all().filter(pk=obj.pk).exists()
        )

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


class IngredientWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )

    def to_internal_value(self, data):
        return super().to_internal_value(data)

class IngredientValueWriteSerializer(serializers.ModelSerializer):
    ingredient = IngredientWriteSerializer()

    class Meta:
        model = IngredientValue
        fields = (
            'ingredient',
            'amount',
        )

    def to_internal_value(self, data):
        data_new = {}
        ingredient = get_object_or_404(Ingredient, pk=data['id'])
        ingredient = IngredientSerializer(ingredient)
        data_new['amount'] = data['amount']
        return data_new

    def save(self, **kwargs):
        return super().save(**kwargs)


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    ingredients = IngredientValueWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        return super().create(validated_data)
