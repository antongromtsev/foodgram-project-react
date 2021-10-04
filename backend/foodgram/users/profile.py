from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


# class ProfileUser(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='profile',
#         verbose_name='Profile user',
#     )
#     subscriptions = models.ManyToManyField(
#         User,
#         related_name='followers',
#         blank=True,
#     )
#     favourites = models.ManyToManyField(
#         Recipe,
#         related_name='fvorites',
#         blank=True,
#     )
#     shopping_list = models.ManyToManyField(
#         Recipe,
#         related_name='shopping',
#         blank=True,
#     )


class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='user_following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='user_followed')


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


class Shopping_cart(models.Model):
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