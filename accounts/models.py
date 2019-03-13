from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('occupation', 'ADMIN')

        if extra_fields.get('occupation') is not 'ADMIN':
            raise ValueError('Superuser must have occupation=ADMIN')
        return super().create_superuser(username, email, password, **extra_fields)


class Profile(AbstractUser):
    OCCUPATION_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('MOD', 'Moderador'),
    )
    occupation = models.CharField('Ocupación', max_length=5, choices=OCCUPATION_CHOICES, default='MOD')

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
