from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField


class RoleChoises(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'


class MyUser(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='First name',
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Last name',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='e-mail',
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Username',
    )

    role = CharField(
        max_length=50,
        choices=RoleChoises.choices,
        default=RoleChoises.USER,
        verbose_name='User role',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    @property
    def is_admin(self):
        return (
            self.role == RoleChoises.ADMIN
            or self.is_staff
            or self.is_superuser
        )

    def __str__(self):
        return '\n'.join([self.username])