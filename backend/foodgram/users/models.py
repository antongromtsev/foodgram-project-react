from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField


class RoleChoises(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'


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

    role = CharField(
        max_length=50,
        choices=RoleChoises.choices,
        default=RoleChoises.USER,
        verbose_name='User role',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    @property
    def is_admin(self):
        return (
            self.role == RoleChoises.ADMIN
            or self.is_staff
            or self.is_superuser
        )

    def __str__(self):
        return '\n'.join([self.username])
