from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from foodgram.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'name', 'text', 'cooking_time',
            'image',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)

    def to_representation(self, instance):
        return RecipeSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount',
        )


class RecipeIngredientPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipePostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = RecipeIngredientPostSerializer(many=True)
    cooking_time = serializers.IntegerField()
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create_ingridients(self, ingredients, recipe):
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=get_object_or_404(Ingredient,
                                                 pk=ingredient.get('id')),
                    amount=ingredient.get('amount')
                ))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingridients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingridients(ingredients, instance)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance, context=self.context
        ).data


class RecipeGetSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientGetSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredient'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('created',)

    def get_is_favorited(self, recipe: Recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.in_cart.filter(recipe=recipe).exists()
