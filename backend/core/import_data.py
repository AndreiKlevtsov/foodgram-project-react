import json

from foodgram.models import Ingredient


def create_models(file_path, model):
    """
    Скрипт выполняется в shell:
    - docker compose exec backend python manage.py shell
    - from foodgram.models import Ingredient
    - from core.import_data import create_models
    - create_models('../data/ingredients.json', Ingredient)
    :param file_path: путь до json файла,
    :param model: модель, импортируется заранее
    """
    with open(
            'data/ingredients.json', encoding='utf-8',
    ) as ingredients_data:
        ingredient_data = json.loads(ingredients_data.read())
        for ingredients in ingredient_data:
            Ingredient.objects.get_or_create(**ingredients)
