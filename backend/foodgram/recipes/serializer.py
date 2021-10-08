from drf_extra_fields.fields import Base64ImageField

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializer import IsSubscribedMixin
from users.models import Favourites, Shopping_cart
from users.serializer import MyUserSerializer

from .models import Ingredient, IngredientValue, Recipe, Tag
from .utils import ingredient_add_recipe


User = get_user_model()


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
        fields = ('ingredient', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = representation['ingredient']
        representation['amount'] = instance.amount

        return representation


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    author = MyUserSerializer()
    ingredients = IngredientValueSerializer(
        source='ingredientvalue_set',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField('get_is_favorited', )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart',
    )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            Favourites.objects.filter(user=user.pk, recipe=obj.pk).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            Shopping_cart.objects.filter(user=user.pk, recipe=obj.pk).exists()
        )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time',
        )


class IngredientValueWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientValue
        fields = ('id', 'amount', )

    def create(self, validated_data):
        self.context
        return super().create(validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientValueWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time',
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context=self.context,
        )
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        obj_recipe = Recipe.objects.create(**validated_data)

        ingredient_add_recipe(ingredients, obj_recipe)

        obj_recipe.save()
        obj_recipe.tags.set(tags)

        return obj_recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientValue.objects.filter(recipe=instance).delete()

        ingredient_add_recipe(ingredients, instance)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.tags.set(tags)
        return instance


class RecipeSubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class UserSubscriptionsSerializer(serializers.ModelSerializer,
                                  IsSubscribedMixin):

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
        recipes_limit = self.context['request'].GET.get('recipes_limit')
        if recipes_limit is None:
            return
        recipes_limit = int(recipes_limit)
        serializers = RecipeSubscriptionsSerializer(
            obj.recipe.reverse()[:recipes_limit],
            many=True,
        )
        return serializers.data

    def get_recipes_count(self, obj):
        return obj.recipe.count()
