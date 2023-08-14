from core.validators import validate_tag_slug
from django.core import validators
from django.db import models
from django.db.models import CASCADE, UniqueConstraint
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        validators=(
            validate_tag_slug,
        )
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.slug} | {self.color}'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор рецепта',
        max_length=256,
        related_name='recipes',
        on_delete=CASCADE,
    )
    name = models.CharField(
        verbose_name='Название',
        unique=True,
        max_length=200,
        blank=False,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images',
        blank=False,
    )
    text = models.TextField(
        verbose_name='Описание',
        blank=False,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        related_name='recipes',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            validators.MinValueValidator(1),
        ),
        blank=False,
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.author.username}, {self.name}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'),
        ),
        default=1,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe',)
        constraints = (
            UniqueConstraint(
                fields=(
                    'recipe',
                    'ingredient',
                ),
                name='unique_ingredients_recipe'),
        )


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец списка",
        related_name="in_cart",
        on_delete=CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепты в списке покупок",
        related_name="in_cart",
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='in_favorites',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipe_user')
        ]
