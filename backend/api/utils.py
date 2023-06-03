from django.db.models import Sum
from django.http import HttpResponse

from recipes.models import IngredientsInRecipe


def create_shopping_cart_file(user):
    sum_ingredients = IngredientsInRecipe.objects.filter(
        recipe__shopping_cart__user=user).values(
        'ingredient__name', 'ingredient__measurement_unit').annotate(
        amounts=Sum('amount'))

    shopping_list = '\n'.join(
        [f'{ingredient["ingredient__name"]} {ingredient["amounts"]} '
         f'{ingredient["ingredient__measurement_unit"]}'
         for ingredient in sum_ingredients])
    response = HttpResponse(shopping_list, content_type='text/plain')
    return response
