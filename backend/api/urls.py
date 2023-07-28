from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.views import CustomUserViewSet, TagViewSet, RecipeViewSet, \
    IngredientViewSet

# from .views import (
#     CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet, UserViewSet
# )

router = SimpleRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register(r'users/subscriptions/', CustomUserViewSet,
                basename='subscriptions')
router.register(r'users/(?P<user_id>\d+)/subscribe/', CustomUserViewSet,
                basename='favourite')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes/(?P<recipes_id>\d+)/shopping_cart/', RecipeViewSet,
                basename='shopping_cart')
router.register(r'recipes/(?P<recipes_id>\d+)/favourite/', RecipeViewSet,
                basename='favourite')



urlpatterns = [
    # path('v1/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
