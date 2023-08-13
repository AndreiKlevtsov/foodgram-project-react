from rest_framework.filters import SearchFilter
from foodgram.models import Ingredient


class IngredientNameFilter(SearchFilter):
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)
