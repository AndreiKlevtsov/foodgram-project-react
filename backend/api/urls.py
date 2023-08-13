from django.urls import include, path
from rest_framework.routers import SimpleRouter
from foodgram.views import TagViewSet, RecipeViewSet, \
    IngredientViewSet
from users.views import CustomUserViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
