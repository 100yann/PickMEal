from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
import requests
import json
import os
from .models import User, RegisterUser, Recipe, Rating
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg




def getRecipes(ingredients):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    api_key = settings.SPOONACULAR_API_KEY

    params = {
    'apiKey': api_key,
    'ingredients': ingredients, 
    'ranking': 1,
    'number': 5
    }



    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    
    data = response.json()
    results = {}
    for recipe in data:
        id = recipe['id']
        title = recipe['title'].title()
        image = recipe['image']
        num_used_ingredients = recipe['usedIngredientCount']
        num_missing_ingredients = recipe['missedIngredientCount']
        missing_ingredients = [j['name'].capitalize() for j in recipe['missedIngredients']]
        used_ingredients = [j['name'].capitalize() for j in recipe['usedIngredients']]
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
            data = response.json()
            
            # format instructions
            instructions = data['instructions']
            fields = {
                'instructions': '',
                'Instructions': '',
                '\n\n': '',
            }
            if instructions:
                for key, value in fields.items():
                    instructions = instructions.replace(key, value)
                
                # make the instructions into an ordered list if they aren't already
                if '<ol>' not in instructions and '<p>' not in instructions:
                    instructions = "<ol><li>" + instructions.replace("\n", "</li><li>") + "</li></ol>"

            recipe_data = {
                'id': recipe_id,
                'title': data['title'],
                'image': data['image'],
                'servings': data['servings'],
                'summary': data['summary'],
                'instructions': instructions,
                # sometimes the API returns duplicate ingredients so ingredients is now a set instead of list
                'ingredients': set(ing['originalName'].capitalize() for ing in data['extendedIngredients'])
                }
            return recipe_data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    

def getTopRecipes():
    top_rated_recipes = Recipe.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:3]
    return top_rated_recipes    
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
        formatted_ings = [x.title() for x in ingredients]
        # recipes = getRecipes(ingredients)
        recipes= {'Goat Cheese Pesto Pizza': {'id': 644953, 'title': 'Goat Cheese Pesto Pizza', 'image': 'https://spoonacular.com/recipeImages/644953-312x231.jpg', 'num_used_ings': 2, 'num_missing_ings': 2, 'missing_ings': ['Pizza Shell', 'Goat Cheese'], 'used_ings': ['Pesto', 'Tomatoes']}, 'Cream Cheese With Sun Dried Tomatoes And Pesto Pastry': {'id': 640513, 'title': 'Cream Cheese With Sun Dried Tomatoes And Pesto Pastry', 'image': 'https://spoonacular.com/recipeImages/640513-312x231.jpg', 'num_used_ings': 2, 'num_missing_ings': 3, 'missing_ings': ['Block Of Cream Cheese', 'Regular Crescents From The Section Of The Grocery', 'Egg - Beat'], 'used_ings': ['Pesto', 'Sundried Tomatoes']}, 'Pesto Fresh Caprese Sandwich': {'id': 655822, 'title': 'Pesto Fresh Caprese Sandwich', 'image': 'https://spoonacular.com/recipeImages/655822-312x231.jpg', 'num_used_ings': 2, 'num_missing_ings': 4, 'missing_ings': ['Balsamic Vinegar', 'Ciabatta Roll', 'Basil Leaves', 'Mozzarella'], 'used_ings': ['Basil Pesto', 'Tomato']}}
        if not recipes:
            # handle error
            ...

        # Get the ids of the returned recipes
        recipe_ids = [recipes[key]['id'] for key in recipes.keys()]

        # Get recipies with the specified IDs and their ratings
        recipes_with_ratings = Recipe.objects.filter(id__in=recipe_ids).annotate(avg_rating=Avg('rating__rating'))
        
        # Get ID and avg rating of each recipe object
        recipe_ratings = {recipe.id: recipe.avg_rating for recipe in recipes_with_ratings}

        # iterate through the returned recipes
        for key, value in recipes.items():
            recipe_id = value['id']
            if recipe_id in recipe_ratings:
                # update the recipe's average rating
                value['avg_rating'] = recipe_ratings[recipe_id]

        return render(request, 'results.html', context={
            'results': recipes,
            'ingredients': ingredients.title()
            })
    

def recipe(request, recipe_id):
    if request.user.id:
        user = User.objects.get(pk=request.user.id)
    else:
        user = False

    # get recipe details
    recipe_data = recipeInformation(recipe_id)
    if Recipe.objects.filter(id=recipe_id).exists():
        recipe = Recipe.objects.get(id=recipe_id)
    else:
        recipe = Recipe.objects.create(id=recipe_id, 
                                        title=recipe_data['title'],
                                        ingredients=recipe_data['ingredients'],
                                        instructions = recipe_data['instructions'],
                                        description=recipe_data['summary'],
                                        servings=recipe_data['servings'],
                                        image=recipe_data['image'])

    if request.method == 'POST':
        data = json.loads(request.body)
        # handle requests that pass if save recipe data
        if 'status' in data:
            is_saved = data.get('status')
            if is_saved == 'false':
                user.saved_recipes.add(recipe.pk)
            elif is_saved == 'true':
                user.saved_recipes.remove(recipe.pk)
            return HttpResponse()
        
        # handle requests that pass rating data
        elif 'rating' in data:
            new_user_rating = data.get('rating')
            recipe_rating = Rating.objects.filter(recipe=recipe, rated_by=user).first()
            if recipe_rating:
                recipe_rating.rating = new_user_rating + 1
                recipe_rating.save()
            else:
                recipe_rating = Rating.objects.create(recipe=recipe, 
                                                      rating=new_user_rating+1, 
                                                      rated_by=user)


    # check if the current user has saved this recipe
    if user:
        if user.saved_recipes.filter(id=recipe_id).exists():
            recipe_saved = True
        else:
            recipe_saved = False
    else:
        recipe_saved = False

    # Get all ratings and average rating for this recipe
    ratings = Rating.objects.filter(recipe=recipe)
    avg_rating = ratings.aggregate(Avg('rating'))

    if ratings.exists():
        # check if the current user has rated this recipe
        user_rating = ratings.filter(rated_by=user).first()
        if user_rating:
            user_rating = user_rating.rating
        else:
            user_rating = False
    else:
        user_rating = False   

    # add necessary fields to recipe_data
    recipe_data['recipe_saved'] = recipe_saved
    recipe_data['user_rating'] = user_rating
    recipe_data['avg_rating'] = avg_rating['rating__avg']
    top_rated_recipes = getTopRecipes()
    recipe_data['top_recipes'] = top_rated_recipes
    return render(request, 'view_recipe.html', recipe_data)


def new_recipe(request):
    if request.method == 'POST':
        # get form data
        title = request.POST.get('recipe-title')
        description = request.POST.get('recipe-description')
        servings = request.POST.get('recipe-servings')
        img = request.POST.get('recipe-img')

        # Get instructions
        instructions = request.POST.getlist('recipe-instructions')

        # Get ingredients
        ingredients = request.POST.getlist('recipe-ingredients')
        print(title, description, servings, instructions, ingredients, sep='\n')
    return render(request, 'new_recipe.html')



def user(request, id):
    recipes_saved = Recipe.objects.filter(users_who_saved=id)
    return render(request, 'user.html', context={
        'recipes': recipes_saved
    })