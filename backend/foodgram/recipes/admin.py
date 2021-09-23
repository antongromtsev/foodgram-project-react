from django.contrib import admin

from .models import Tag, Recipe, IngredientValue, Ingredient


class IngredientValueInline (admin.TabularInline):
    model = IngredientValue
    extra = 1


class IngredientValueAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe", "value")
    search_fields = ("ingredient",)
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("slug",)
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "name",
        "image",
        "text",
        "get_ingredients",
        "get_tags",
    )
    search_fields = ("slug",)
    empty_value_display = "-пусто-"
    inlines = (IngredientValueInline,)


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientValue, IngredientValueAdmin)
