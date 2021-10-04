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

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    measurement_unit = models.CharField(
        max_length=50,
        default='г'
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=250,
    )
    image = models.ImageField(upload_to='recipes')
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientValue',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publication date',
    )

    class Meta:
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
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1), ]
    )
