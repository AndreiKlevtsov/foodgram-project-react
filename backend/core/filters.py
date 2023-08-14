from foodgram.models import Ingredient
from rest_framework.filters import SearchFilter


class IngredientNameFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)
