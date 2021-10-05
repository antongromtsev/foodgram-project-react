from django.contrib import admin

from .models import Ingredient, IngredientValue, Recipe, Tag


class IngredientValueInline (admin.TabularInline):
    model = IngredientValue
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("slug",)
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "added_to_favorites",
    )
    list_filter = ("author", "name", "tags")
    empty_value_display = "-пусто-"
    inlines = (IngredientValueInline,)

    def added_to_favorites(self, obj):
        result = obj.favorites.count()
        return result


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
