import django_filters
from django_filters import rest_framework as filters

from .models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name='author__pk',
        lookup_expr='contains',
    )
    tags = filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = django_filters.BooleanFilter(method='filter')
    is_in_shopping_cart = django_filters.BooleanFilter(method='filter')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated or not value:
            return queryset
        elif name == 'is_favorited':
            return queryset.filter(favorites__user=user)
        return queryset.filter(shopping_cart__user=user)
