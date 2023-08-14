from core.pagination import LimitPagePagination
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import CustomUser, Subscription

from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          SubscriptionsSerializer)


class CustomUserViewSet(UserViewSet):
    """
    Представление для управления пользователями.
    """
    queryset = CustomUser.objects.all()
    pagination_class = LimitPagePagination

    def get_serializer_class(self):
        """
        Возвращает нужный сериализатор,
            основываясь на методе или action запроса.
        :return: Serializer class
        """
        if self.action == 'subscriptions':
            return SubscriptionsSerializer
        if self.request.method.lower() == 'post':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(
        detail=False, methods=('get',),
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        """
        Показывает информацию текущего авторизованного пользователя.
        :param request: HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Response.
        """
        self.get_object = self.get_instance
        user = self.request.user
        return Response(CustomUserSerializer(
            user,
            context={'request': request}
        ).data)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        """
        Подписка на пользователя.
        :param request: HTTP request object.
        :param id: (int): id автора, на которого оформляется пописка.
        :return: Response.
        """
        author = get_object_or_404(CustomUser, id=id)
        user = request.user
        if user == author:
            return Response(
                {'errors': 'Нельзя подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(username=user,
                                       author=author).exists():
            return Response(
                {'errors': 'Вы уже подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(username=user, author=author)
        return Response(CustomUserSerializer(
            author,
            context={'request': request}
        ).data)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        """
        Отписка от пользователя.
        """
        author = get_object_or_404(CustomUser, id=id)
        user = request.user
        subscription = Subscription.objects.filter(
            username=user,
            author=author,
        )
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {"errors": "Вы не подписаны на данного пользователя"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """
        Список подписок текущего пользователя.
        :param request: HTTP request object.
        :return: Response.
        """
        subscribing_users = request.user.subscribe.values_list(
            'author_id', flat=True)
        subscriptions = CustomUser.objects.filter(id__in=subscribing_users)
        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)
