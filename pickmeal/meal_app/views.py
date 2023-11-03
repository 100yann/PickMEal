from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json
import os
from .models import User, RegisterUser
from django.contrib.auth import authenticate, login, logout




def getRecipes(ingredients):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    api_key = settings.SPOONACULAR_API_KEY

    params = {
    'apiKey': api_key,
    'ingredients': ingredients, 
    'ranking': 1,
    'number': 3
    }



    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    
    data = response.json()
    recipe_ids = ''
    results = {}
    for recipe in data:
        id = recipe['id']
        recipe_ids += f'{id},'
        title = recipe['title'].title()
        image = recipe['image']
        num_used_ingredients = recipe['usedIngredientCount']
        num_missing_ingredients = recipe['missedIngredientCount']
        missing_ingredients = [j['name'].title() for j in recipe['missedIngredients']]
        used_ingredients = [j['name'].title() for j in recipe['usedIngredients']]
        results[title] = {
            'id': id,
            'title': title,
            'image': image,
            'num_used_ings': num_used_ingredients,
            'num_missing_ings': num_missing_ingredients,
            'missing_ings': missing_ingredients,
            'used_ings': used_ingredients
        }
    return results


def recipeInformation(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    api_key = settings.SPOONACULAR_API_KEY
    params = {
        'apiKey': api_key
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    

# Create your views here.
def index(request):
    return render(request, 'index.html')


def log_out(request):
    logout(request)
    return redirect('home')


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'sign_in.html', {
                'message': 'Invalid username and/or password.'
            })
    return render(request, 'sign_in.html')

def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password'] 

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('home')
        else:
            # If form isn't valid return error messages
            return render(request, 'register.html', {
                'form': form,
                })
            

    form = RegisterUser
    return render(request, 'register.html', {
        'form': form
    })

def results(request):
    if request.method == 'POST':
        data = request.POST
        ingredients = data.get('recipe-search')
        # recipes = getRecipes(ingredients)
        recipes= {'Goat Cheese Pesto Pizza': {'id': 644953, 'title': 'Goat Cheese Pesto Pizza', 'image': 'https://spoonacular.com/recipeImages/644953-312x231.jpg', 'num_used_ings': 2, 'num_missing_ings': 2, 'missing_ings': ['Pizza Shell', 'Goat Cheese'], 'used_ings': ['Pesto', 'Tomatoes']}, 'Cream Cheese With Sun Dried Tomatoes And Pesto Pastry': {'id': 640513, 'title': 'Cream Cheese With Sun Dried Tomatoes And Pesto Pastry', 'image': 'https://spoonacular.com/recipeImages/640513-312x231.jpg', 'num_used_ings': 2, 'num_missing_ings': 3, 'missing_ings': ['Block Of Cream Cheese', 'Regular Crescents From The Section Of The Grocery', 'Egg - Beat'], 'used_ings': ['Pesto', 'Sundried Tomatoes']}, 'Pesto Fresh Caprese Sandwich': {'id': 655822, 'title': 'Pesto Fresh Caprese Sandwich', 'image': 'https://spoonacular.com/recipeImages/655822-312x231.jpg', 'num_used_ings': 2, 'num_missing_ings': 4, 'missing_ings': ['Balsamic Vinegar', 'Ciabatta Roll', 'Basil Leaves', 'Mozzarella'], 'used_ings': ['Basil Pesto', 'Tomato']}}
        
        if not recipes:
            # handle error
            ...
        # json_file_path = os.path.join(settings.BASE_DIR, 'meal_app/static', 'working_data.json')

        # with open(json_file_path, 'r') as file:
        #     recipes = json.load(file)

        return render(request, 'results.html', context={
            'results': recipes
            })
def recipe(request, recipe_id):
    
    # get recipe details
    print(recipeInformation(recipe_id))
    return render(request, 'view_recipe.html', {})