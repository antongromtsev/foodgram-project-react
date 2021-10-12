from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Name ingredient',
    )
    measurement_unit = models.CharField(
        max_length=50,
        default='г',
        verbose_name='Measurenet unit',
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['name', 'measurement_unit'],
        #         name='unique_ingredient',
        #     )
        # ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='Author recipe',
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Name recipe',
    )
    image = models.ImageField(
        upload_to='recipes',
        verbose_name='Image'
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientValue',
        verbose_name='Ingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Tags',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), ],
        verbose_name='Cooking time',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publication date',
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name

    def get_ingredients(self):
        return ', '.join(
            [ingredient.name for ingredient in self.ingredients.all()]
        )

    def get_tags(self):
        return ', '.join([tags.name for tags in self.tags.all()])


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1), ],
        verbose_name='Ingredient amount',
    )

    class Meta:
        verbose_name = 'Ingredient amount'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe',
            )
        ]

    def __str__(self):
        return str(self.ingredient)
