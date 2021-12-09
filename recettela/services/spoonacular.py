import json
import operator

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from recettela.models import Food


def food_list(request):
    r = requests.get('http://www.themealdb.com/api/json/v1/1/list.php?i=list')
    if r.status_code == 200:
        json_food = r.json()
        for element in json_food['meals']:  # Simplifier le json pour obtenir seulement le nom et id
            element.pop('strDescription', None)
            element.pop('strType', None)
        # list_food = list(map(operator.itemgetter('strIngredient'), json_food['meals']))
        return JsonResponse(json_food)


# def recipe_list(request):

@login_required
def reverse_recipe(request):
    user = request.user
    foods_fridge_user = Food.objects.filter(fridge=user)
    str_food = ""
    for food in foods_fridge_user:
        str_food += food.__str__() + ",+"
    str_food = str_food[:-2]

    r = requests.get(
        'https://api.spoonacular.com/recipes/findByIngredients?ingredients=' + str_food + '&apiKey=04a5aef53bd442d28f3338d9b852be8b&includeNutrition=true')
    if r.status_code == 200:
        json_food = r.json()
        return JsonResponse(json_food, safe=False)


@login_required
def search_recipe(request):
    r = requests.get(
        'https://api.spoonacular.com/recipes/complexSearch?query=' + request.GET.get('query', '') + '&apiKey=04a5aef53bd442d28f3338d9b852be8b')
    if r.status_code == 200:
        json_food = r.json()
        return JsonResponse(json_food['results'], safe=False)
