import django_filters

from .models import Ingredient, Recipe


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
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='contains',
    )
    is_favorited = django_filters.BooleanFilter(method='filter')
    is_in_shopping_cart = django_filters.BooleanFilter(method='filter')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated or value is False:
            return queryset
        if name == 'is_favorited':
            return queryset.filter(fvorites__user=user)
        if name == 'is_in_shopping_cart':
            return queryset.filter(shopping__user=user)
