from djoser.serializers import UserCreateSerializer, UserSerializer
from foodgram.models import Recipe
from rest_framework import serializers
from users.models import CustomUser, Subscription


class RecipeSerializerForUser(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = Recipe
        fields = (
            'name', 'text', 'cooking_time',
            'image',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """

    """

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'password',
            'username', 'first_name', 'last_name'
        )
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserSerializer(UserSerializer):
    """

    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        """
        Возвращает флаг, указывающий, подписан ли пользователь на автора.

        :param obj: Объект автора.
        :type obj: CustomUser
        :return: Флаг, указывающий, подписан ли пользователь на автора.
        :rtype: bool
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(
            username=user,
            author=obj
        ).exists()


class SubscriptionsSerializer(CustomUserSerializer):
    """

    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        """
        Возвращает список рецептов, принадлежащих пользователю.

        :param obj: Объект пользователя.
        :type obj: CustomUser

        :return: Список сериализованных рецептов пользователя.
        :rtype: List[dict]
        """
        limit = self.context.get('request').GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSerializerForUser(queryset, many=True).data

    def get_recipes_count(self, obj):
        """
        Возвращает общее количество рецептов, принадлежащих пользователю.

        :param obj: Объект пользователя.
        :type obj: CustomUser

        :return: Общее количество рецептов пользователя.
        :rtype: int
        """
        return obj.recipes.count()
