from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import Favourites, ShoppingCart
from users.serializer import IsSubscribedMixin, UserRepresentationSerializer

from .models import Ingredient, IngredientValue, Recipe, Tag
from .utility import ingredient_add_recipe

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
    author = UserRepresentationSerializer()
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
            user.is_authenticated
            and Favourites.objects.filter(user=user.pk, recipe=obj.pk).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(
                user=user.pk,
                recipe=obj.pk).exists()
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
    amount = serializers.IntegerField(error_messages={
        'invalid':
        'Количество ингредиента должно быть целым, положительным числом!'
    })

    class Meta:
        model = IngredientValue
        fields = ('id', 'amount', )


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientValueWriteSerializer(many=True)
    cooking_time = serializers.IntegerField(error_messages={
        'invalid':
        'Время приготовления должно быть целым, положительным числом!'
    })

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

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        correct_ingredients = []
        for item in ingredients:
            if correct_ingredients.count(item['id']):
                raise serializers.ValidationError({
                    'ingredients': 'В рецепте дублирующиеся ингредиенты!'
                })
            else:
                correct_ingredients.append(item['id'])
            if int(item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients':
                    'Убедитесь, что значение количества ингредиента больше 0!'
                })
            
        cooking_time = self.initial_data.get('cooking_time')
        if cooking_time <= 0:
            raise serializers.ValidationError({
                'cooking_time':
                'Значение времени не может быть меньше нуля!'
            })
        return data

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
            return None
        recipes_limit = int(recipes_limit)
        serializers = RecipeSubscriptionsSerializer(
            obj.recipe.reverse()[:recipes_limit],
            many=True,
        )
        return serializers.data

    def get_recipes_count(self, obj):
        return obj.recipe.count()
