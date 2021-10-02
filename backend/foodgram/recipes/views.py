from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Avg
from django.db.models import Sum
from django.db.models import F

from .models import Tag, Recipe, Ingredient
from .serializer import TagSerializer, RecipeSerializer, RecipeWriteSerializer, IngredientSerializer
from .filters import IngredientFilter, RecipeFilter
from users.pagination import PaginationLimit
from users.serializer import RecipeSubscriptionsSerializer

class MixinRetrieveList(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class IngredientViewSet(MixinRetrieveList):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = IngredientFilter


class TagViewSet(MixinRetrieveList):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PaginationLimit
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'get':
            return RecipeSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(['get', 'delete'], detail=True, url_path='favorite')
    def favorite(self, request, pk=None):
        user = request.user
        recipe_fav = get_object_or_404(Recipe, pk=int(pk))
        if request.method == 'DELETE':
            user.profile.favourites.remove(recipe_fav.pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        user.profile.favourites.add(recipe_fav)
        serializer = RecipeSubscriptionsSerializer(
            recipe_fav,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['get', 'delete'], detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe_shop = get_object_or_404(Recipe, pk=int(pk))
        if request.method == 'DELETE':
            user.profile.shopping_list.remove(recipe_shop.pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        user.profile.shopping_list.add(recipe_shop)
        serializer = RecipeSubscriptionsSerializer(
            recipe_shop,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(['get'], detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        user = request.user
        user_cart = user.profile.shopping_list.all()
        user_cart_ing = user_cart.values('ingredients__name', 'ingredients__measurement_unit', 'ingredientvalue__amount')

#  Task.objects.aggregate(total=Sum(F('progress') * F('estimated_days')))['total']
        shopping_cart={}
        for ingredient in user_cart_ing:
            keys = ingredient['ingredients__name']
            if keys not in shopping_cart.keys():
                shopping_cart[keys] = ingredient
            else:
                shopping_cart[keys]['ingredientvalue__amount'] += ingredient['ingredientvalue__amount']
                
        return Response(status=status.HTTP_201_CREATED)