from core.validators import validate_username
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        validators=(validate_username,)
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Subscription(models.Model):
    username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='subscribe',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "username",
                    "author",
                ),
                name="unique_follow", )
        ]
