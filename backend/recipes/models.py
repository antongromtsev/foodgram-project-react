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


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    measurement_unit = models


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
        on_delete=models.SET_NULL,
    )
    cooking_time = models.IntegerField(
        validators=MinValueValidator(1),
    )


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
        validators=MinValueValidator(1),
    )