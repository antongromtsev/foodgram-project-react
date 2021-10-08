from .models import IngredientValue


def ingredient_add_recipe(ingredients, obj):
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
