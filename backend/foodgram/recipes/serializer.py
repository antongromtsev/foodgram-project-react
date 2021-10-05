import base64
import imghdr
import uuid
import six

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from users.mixin import IsSubscribedMixin
from users.profile import Favourites, Shopping_cart
from users.serializer import MyUserSerializer

from .models import Ingredient, IngredientValue, Recipe, Tag

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = '%s.%s' % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = 'jpg' if extension == 'jpeg' else extension

        return extension


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

        igredient_add_recipe(ingredients, obj_recipe)

        obj_recipe.save()
        obj_recipe.tags.set(tags)

        return obj_recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientValue.objects.filter(recipe=instance).delete()

        igredient_add_recipe(ingredients, instance)

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
            obj.recipe.order_by('-pub_date')[:recipes_limit],
            many=True,
        )
        return serializers.data

    def get_recipes_count(self, obj):
        return obj.recipe.count()


def igredient_add_recipe(ingredients, obj):
    recipe_ing = {}

    for item in ingredients:
        name_ing = item['id'].name
        if name_ing not in recipe_ing:
            recipe_ing[name_ing] = IngredientValue.objects.create(
                ingredient=item['id'],
                recipe=obj,
                amount=item['amount']
            )
            obj.ingredients.add(item['id'])
        else:
            recipe_ing[name_ing].amount += item['amount']
            recipe_ing[name_ing].save()
