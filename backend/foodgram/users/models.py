from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField


class MyUser(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='First name',
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Last name',
        blank=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='e-mail',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Username',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return '\n'.join([self.username])
