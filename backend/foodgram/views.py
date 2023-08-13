import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from core.filters import IngredientNameFilter
from core.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    RecipeGetSerializer, RecipePostSerializer,
    RecipeSerializer, FavoriteSerializer
)
from rest_framework.decorators import action
from foodgram.models import Recipe, Ingredient, Tag, Favorite, Cart
from .serializers import TagSerializer, IngredientSerializer
from core.pagination import LimitPagePagination
from core.shopping_cart_service import (
    get_ingredients, generate_final_list,
    draw_shopping_cart
)


class RecipeViewSet(ModelViewSet):
    """
    Получение списка всех рецептов, добавлеиние, редактирование и удаление.
    - `permission_classes` определяет классы разрешений,
        необходимые для доступа к представлению.
        В этом случае класс `IsAdminOrAuthorOrReadOnly` предоставляет
        администраторам полный доступ,
        гостям ReadOnly,
        авторам права на добавление, редактирование, удаление своего рецепта.
    - `pagination_class` определяет используемый стиль разбивки на страницы.
    """
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    pagination_class = LimitPagePagination
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        """
        :param serializer:
            (RecipePostSerializer): Сериализатор для создания рецепта.
        :return: None
        """
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """
        Возвращает нужный сериализатор, основываясь на методе запроса.
        :return: Serializer class
        """
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipePostSerializer

    def get_queryset(self):
        """
        Возвращает queryset, основываясь на параметрах запроса.
        :return: Queryset.
        """
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited:
            return Recipe.objects.filter(in_favorites__user=self.request.user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart:
            return Recipe.objects.filter(in_cart__user=self.request.user)
        tags = self.request.query_params.getlist('tags')
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags)
        return Recipe.objects.all()

    @action(detail=True, methods=('post',))
    def favorite(self, request, pk=None):
        """
        Добавляет рецепт в список избранного пользователя.
        :param request: HTTP request object.
        :param pk: pk рецепта, переданный в запросе.
        :return: Response.
        """
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe,
        )
        if favorite.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response(FavoriteSerializer(
            recipe,
            context={'request': request}
        ).data)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk=None):
        """
        Удаляет рецепт из списка избранного.
        """
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe,
        )
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {'errors': 'Рецепт не находится в избранном'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('post',), )
    def shopping_cart(self, request, pk=None):
        """
        Добваляет рецепт в список покупок.
        :param request: HTTP request object.
        :param pk: pk рецепта, переданный в запросе.
        :return: Response.
        """
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = Cart.objects.filter(
            user=request.user,
            recipe=recipe,
        )
        if shopping_cart.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        Cart.objects.create(user=request.user, recipe=recipe)
        return Response(RecipeSerializer(
            recipe,
            context={'request': request}
        ).data)

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk=None):
        """
        Удаляет рецепт из списока покупок.
        """
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = Cart.objects.filter(
            user=request.user,
            recipe=recipe,
        )
        if shopping_cart.exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {'errors': 'Рецепт не находится в списке покупок'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def download_shopping_cart(self, request):
        """
        :param request: HTTP request object.
        :return: HttpResponse.
        """
        ingredients = get_ingredients(user_id=request.user.id)
        shopping_cart = generate_final_list(ingredients)
        font_path = os.path.join(
            settings.BASE_DIR,
            'core/HelveticaBlack.ttf'
        )
        pdfmetrics.registerFont(TTFont('HelveticaBlack', font_path, 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.pdf"'
        page = canvas.Canvas(response)
        draw_shopping_cart(page, shopping_cart)
        page.showPage()
        page.save()
        return response


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    - `queryset` представляет набор объектов ингредиентов,
        к которым необходимо получить доступ.
    - `permission_classes` определяет классы разрешений,
        необходимые для доступа к представлению.
        В этом случае класс `IsAdminOrReadOnly` предоставляет администраторам
        полный доступ, в то время как другие имеют доступ только для чтения.
    - `filter_backends`: Настроенный серверный модуль фильтра
        для фильтрации ингредиентов по названию.
    - `search_fields`: Поле `name' используется для поиска названия ингредиента
        начинающегося с указанного значения.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientNameFilter,)
    search_fields = ('^name',)


class TagViewSet(ReadOnlyModelViewSet):
    """
    - `queryset` представляет набор объектов тегов,
        к которым необходимо получить доступ.
    - `permission_classes` определяет классы разрешений,
        необходимые для доступа к представлению.
        В этом случае класс `IsAdminOrReadOnly` предоставляет администраторам
        полный доступ, в то время как другие имеют доступ только для чтения.
    - `pagination_class` определяет используемый стиль разбивки на страницы.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
