from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import SET_NULL, CASCADE

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тег',
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        max_length=256,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=SET_NULL,
        null=True,
    )
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(1),)
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    amount = models.FloatField(validators=(MinValueValidator(0.1),))


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Объект подписки'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепты в списке покупок",
        related_name="in_carts",
        on_delete=CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец списка",
        related_name="carts",
        on_delete=CASCADE,
    )
    added = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, editable=False
    )


class Favourite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранное',
        on_delete=CASCADE,
        related_name='in_favorites'
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='favorites',
        on_delete=CASCADE,
        verbose_name='Пользователь'
    )
