from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from .models import Tag, Recipe, Ingredient, IngredientValue
from users.serializer_user import MyUserSerializer


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



class IngredientValueWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    # amount = serializers.IntegerField(
    #     min_value=1,
    #     error_messages={
    #         'min_value': 'Разрешено только целое положительное число!'
    #     }
    # )
    class Meta:
        model = IngredientValue
        fields = (
            'id',
            'amount',
        )

    def create(self, validated_data):
        self.context
        return super().create(validated_data)

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

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context=self.context
        )
        return serializer.data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        obj_recipe = Recipe.objects.create( **validated_data)

        recipe_ing = {}
    
        for item in ingredients:
            name_ing = item['id'].name
            if name_ing not in recipe_ing:
                recipe_ing[name_ing] = IngredientValue.objects.create(
                    ingredient=item['id'],
                    recipe=obj_recipe,
                    amount=item['amount']
                )    
                obj_recipe.ingredients.add(item['id'])
            else:
                recipe_ing[name_ing].amount += item['amount']
                recipe_ing[name_ing].save()          
        
        obj_recipe.tags.set(tags)

        return obj_recipe
