from django.contrib.auth import get_user_model
from django.db import models
from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='following')
    user_sub = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='followed')

    class Meta:
        verbose_name = 'Following user'
        verbose_name_plural = 'Following users'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'user_sub'],
                name='unique_following'
            )
        ]


class Favourites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Favorite recipe'
        verbose_name_plural = 'Favorite recipes'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_cart'
            )
        ]
