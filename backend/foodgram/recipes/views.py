from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from collections import defaultdict

from recipes.serializer import RecipeSubscriptionsSerializer

from users.profile import Shopping_cart, Favourites
from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .pagination import PaginationLimit
from .permissions import IsAuthorAdminOrReadOnly
from .serializer import (IngredientSerializer, RecipeSerializer,
                         RecipeWriteSerializer, TagSerializer)


class MixinRetrieveList(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
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
    permission_classes = [IsAuthorAdminOrReadOnly, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'get':
            return RecipeSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        ['get', 'delete'], detail=True,
        url_path='favorite', permission_classes=[IsAuthorAdminOrReadOnly]
    )
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

    @action(
        ['get', 'delete'], detail=True,
        url_path='shopping_cart', permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe_shop = get_object_or_404(Recipe, pk=int(pk))
        if request.method == 'DELETE':
            Shopping_cart.objects.filter(user=user, recipe=recipe_shop).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Shopping_cart.objects.get_or_create(user=user, recipe=recipe_shop)
        serializer = RecipeSubscriptionsSerializer(
            recipe_shop,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        ['get'], detail=False,
        url_path='download_shopping_cart', permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        cart_ingredients = Recipe.objects.filter(shopping_cart__user=request.user).all().values(
            'ingredients__name',
            'ingredients__measurement_unit',
            'ingredientvalue__amount'
        )

        dick = {
            'name': '',
            'unit': '',
            'amount': 0,
        }

        shopping_cart = defaultdict(dick)

        for ing in cart_ingredients:
            #key = ing['ingredients__name'] + f' ({ing["ingredients__measurement_unit"]}) -'
            shopping_cart = shopping_cart[ing['ingredients__name']]
            shopping_cart['name'] = ing['ingredients__name']
            shopping_cart['unit'] = ing['ingredients__measurement_unit']
            shopping_cart['amount'] += ing['ingredientvalue__amount']
            # keys = ingredient['ingredients__name']
            # if keys not in shopping_cart.keys():
            #     shopping_cart[keys] = ingredient
            # else:
            #     value = ingredient['ingredientvalue__amount']
            #     shopping_cart[keys]['ingredientvalue__amount'] += value

        # content = ([f'{item["ingredients__name"]}'
        #             f' ({item["ingredients__measurement_unit"]}) '
        #             f'- {item["ingredientvalue__amount"]}\n'
        #             for item in shopping_cart.values()])
        x = shopping_cart.keys()
        content = ([item + f'{x}' for item in shopping_cart])
        response = HttpResponse(
            content,
            content_type='text/plain',
            status=status.HTTP_201_CREATED
        )

        return response
