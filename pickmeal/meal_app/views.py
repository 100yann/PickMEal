from django.shortcuts import render
from django.conf import settings
from django.templatetags.static import static
import requests
import json
import os


def getRecipes(ingredients):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    api_key = settings.SPOONACULAR_API_KEY

    params = {
        'apiKey': api_key,
        'ingredients': ingredients,
        'number': 5
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Create your views here.
def index(request):
    if request.method == 'POST':
        data = request.POST
        ingredients = data.get('recipe-search')
        # recipes = getRecipes(ingredients)
        # if not recipes:
        #     # handle error
        #     ...
        json_file_path = os.path.join(settings.BASE_DIR, 'meal_app/static', 'working_data.json')

        with open(json_file_path, 'r') as file:
            recipes = json.load(file)

        results = [{'title': item['title'], 'image': item['image'], 'missed_ingredients': item['missedIngredients']} for item in recipes]
        print(results)
        # return render(request, 'results.html', context=results)
    return render(request, 'index.html')