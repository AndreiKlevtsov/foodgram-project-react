from django.db.models import Sum
from foodgram.models import Ingredient


def get_ingredients(user_id):
    """
    Получает ингридиенты из рецептов, добавленных в список покупок.
    :param user_id: ID пользователя.
    :return: QuerySet с суммой всех ингредиентов в списке покупок.
    """
    return Ingredient.objects.filter(
        recipeingredient__recipe__in_cart__user=user_id
    ).select_related('recipeingredient').annotate(
        amount=Sum('recipeingredient__amount')
    ).values('name', 'amount', 'measurement_unit')


def generate_final_list(ingredients):
    """
    Создает список покупок с ингридиентами.
    :param ingredients: QuerySet с суммой всех ингредиентов.
    :return:
        dict: Финальный список покупок с названиями ингредиентов 'keys'
        и количеством/единицами измерения 'values'
    """
    shopping_cart = {}
    shopping_cart = {
        item['name']: {
            'measurement_unit': item['measurement_unit'],
            'amount': item['amount']
        } if item['name'] not in shopping_cart
        else {
            'measurement_unit': item['measurement_unit'],
            'amount': shopping_cart[item['name']]['amount'] + item[
                'amount']
        }
        for item in ingredients
    }
    return shopping_cart


def draw_shopping_cart(page, shopping_cart):
    """
    Создает список на PDF странице, используется библиотека 'reportlab'.
    :param page: canvas.Canvas: PDF страница для разметки.
    :param shopping_cart:
        Dict: Представление 'shopping cart',
        возвращаемое функцией 'generate_final_list()'.
    :return:
    """
    page.setFont('HelveticaBlack', 14)
    page.drawString(100, 800, 'Список ингридиентов:')
    height = 750
    for position, (name, data) in enumerate(shopping_cart.items(), 1):
        amount = str(data['amount'])
        measurement_unit = data['measurement_unit']
        page.drawString(
            100, height, (
                f'{position}. {name} - {amount}, {measurement_unit}'
            )
        )
        height -= 20
