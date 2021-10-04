from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class ProfileUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Profile user',
    )
    subscriptions = models.ManyToManyField(
        User,
        related_name='followers',
        blank=True,
    )
    favourites = models.ManyToManyField(
        Recipe,
        related_name='fvorites',
        blank=True,
    )
    shopping_list = models.ManyToManyField(
        Recipe,
        related_name='shopping',
        blank=True,
    )
