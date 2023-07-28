from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404

from users.serializers import UserSerializer, RecipeGetSerializer, \
    RecipePostSerializer
from users.models import CustomUser
from foodgram.models import Recipe, Ingredient, Follow, Tag, RecipeIngredient, \
    Favourite, Cart

from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, TagSerializer, \
    IngredientSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = ''
    # pagination_class = ''


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipePostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeGetSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        return Response(
            serializer.data, status=HTTP_201_CREATED
        )


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = ''
    # pagination_class = ''


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = ''
    # pagination_class = ''
