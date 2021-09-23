from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
    )
    color = models.CharField(
        max_length=7,
    )
    slug = models.SlugField(
        unique=True
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
    image = models.FileField(
        upload_to='image/',
    )
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

    def get_ingredients(self):
        return ', '.join([ingredient.name for ingredient in self.ingredients.all()])

    def get_tags(self):
        return ', '.join([tags.name for tags in self.tags.all()])

    def __str__(self):
        return self.name



class IngredientValue(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        validators=[MinValueValidator(1), ]
    )


class ProfileUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Profile user',
    )
    subscriptions = models.ManyToManyField(
        User,
        related_name='followers',
    )
    favourites = models.ManyToManyField(
        Recipe,
        related_name='fvorites',
    )
    shopping_list = models.ManyToManyField(
        Recipe,
        related_name='shopping',
    )
