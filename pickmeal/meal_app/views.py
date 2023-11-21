from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
import requests
import json
import os
from .models import User, RegisterUser, Recipe, Rating, NewRecipe, RecipeDetails, RecipeDietaryTags
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
import time


SPOONACULAR_APIS = {
    'findByIngredients': 'https://api.spoonacular.com/recipes/findByIngredients',
    'advancedSearch': 'https://api.spoonacular.com/recipes/complexSearch',
}

RECIPE_DATA_FIELDS = {
    'search_by_ingredients': {
        'id': 'id',
        'image': 'image',
        'num_used_ingredients': 'usedIngredientCount',
        'num_missing_ingredients': 'missedIngredientCount'
    },
    'advanced_search': {
        'id': 'id',
        'image': 'image',
    },
    'recipe_details': {
        'id': 'id',
        'title': 'title',
        'image': 'image',
        'servings': 'servings',
        'summary': 'summary',
        'cooking_time': 'readyInMinutes',
        'is_vegan': 'vegan',
        'is_vegetarian': 'vegetarian',
        'is_dairy_free': 'dairyFree',
        'is_gluten_free': 'glutenFree'
    }
}

def get_recipes(url, recipe_id=None, **parameters):
    api_key = settings.SPOONACULAR_API_KEY
    params = {
        'apiKey': api_key
    }

    # update params
    for key, value in parameters.items():
        params[key] = value

    try:
        response = requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    else:
        if response.status_code == 200:
            data = response.json()
            return data

    
def unpack_recipe_data(data, **fields):
    results = {}

    try:
        data = data['results']
    except (KeyError, TypeError):
        pass
    
    if type(data) == list:
        for recipe in data:
            title = recipe['title'].title()
            results[title] = {}
            for key, value in fields.items():
                results[title][key] = recipe[value]
            
            try:
                results[title]['missing_ings'] = [j['name'].capitalize() for j in recipe['missedIngredients']]
                results[title]['used_ings'] = [j['name'].capitalize() for j in recipe['usedIngredients']]
            except (KeyError, TypeError):
                pass
    
    else:
        for key, value in fields.items():
            results[key] = data[value]
        results['instructions'] = format_instructions(data['instructions'])
        results['ingredients'] = format_ingredients(data['extendedIngredients'])

    return results

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


# format recipe instructions
def format_instructions(instructions):
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
    return instructions


# format recipe ingredients
def format_ingredients(ingredients):
    # sometimes the API returns duplicate ingredients so ingredients 
    # is now a set instead of list
    return set(ing['originalName'].capitalize() for ing in ingredients)


# get detailed recipe information from
# spoonacular API
def recipeInformation(recipe_id):
    api_key = settings.SPOONACULAR_API_KEY
    params = {
        'apiKey': api_key
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            recipe_data = {
                'id': recipe_id,
                'title': data['title'],
                'image': data['image'],
                'servings': data['servings'],
                'summary': data['summary'],
                'cooking_time': data['readyInMinutes'],
                'instructions': format_instructions(data['instructions']),
                'ingredients': format_ingredients(data['extendedIngredients']),
                'dietary_tags': {'vegetarian': data['vegetarian'],
                                 'vegan': data['vegan'],
                                 'dairy_free': data['dairyFree'],
                                 'gluten_free': data['glutenFree']}
                }
            return recipe_data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    

def getAdvancedRecipe(ingredients, diet=None, intolerances=None, prep_time=None):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    api_key = settings.SPOONACULAR_API_KEY
    params = {
        'query': ingredients,
        'apiKey': api_key,
        'number': 3
    }

    if diet:
        params['diet'] = diet
    if intolerances: 
        params['intolerances'] = intolerances
    if prep_time:
        params['maxReadyTime'] = prep_time

    try:
        response = requests.get(url, params)
        if response.status_code == 200:
            data = response.json()
            results = {}
            for recipe in data['results']:
                title = recipe['title']
                results[title] = {
                    'id': recipe['id'],
                    'title': title,
                    'image': recipe['image']
                }
            return results
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    
# Create your views here.
def index(request):
    return render(request, 'index.html')


def advanced_search(request):
    return render(request, 'advanced_search.html')


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

        prep_time = request.POST.get('prep-time', '')
        if prep_time: 
            is_vegan = 'vegan' in request.POST
            is_vegetarian = 'vegetarian' in request.POST
            is_dairy_free = 'dairy-free' in request.POST
            is_gluten_free = 'gluten-free' in request.POST
            
            url = SPOONACULAR_APIS['advancedSearch']
            params = {
                'query': ingredients,
                'number': 6,
                }

            if is_vegan:
                params['diet'] = params.get('diet', '') + 'vegan,'
            if is_vegetarian:
                params['diet'] = params.get('diet', '') + 'vegetarian,'

            if is_dairy_free:
                params['intoleranceds'] = params.get('diet', '') + 'dairy,'
            if is_gluten_free:
                params['intoleranceds'] = params.get('diet', '') + 'gluten,'

            if prep_time:
                params['maxReadyTime'] = prep_time

            data = get_recipes(url, **params)
            fields = RECIPE_DATA_FIELDS['advanced_search']
                
        else:
            url = SPOONACULAR_APIS['findByIngredients']
            params = {
                'ingredients': ingredients,    
                'ranking': 1,
                'number': 6
            }
            data = get_recipes(url, **params)
            fields = RECIPE_DATA_FIELDS['search_by_ingredients']
        
        recipes = unpack_recipe_data(data, **fields)
        message = None
        if not recipes:
            message = 'No recipes found that match the criteria, please refine your search'
        # Get the ids of the returned recipes
        # recipe_ids = [recipes[key]['id'] for key in recipes.keys()]

        # Get recipies with the specified IDs and their ratings
        # recipes_with_ratings = Recipe.objects.filter(spoonacular_id__in=recipe_ids).annotate(avg_rating=Avg('ratings__rating'))
        
        # Get ID and avg rating of each recipe object
        # recipe_ratings = {recipe.id: recipe.avg_rating for recipe in recipes_with_ratings}

        # iterate through the returned recipes
        # for key, value in recipes.items():
        #     recipe_id = value['id']
        #     if recipe_id in recipe_ratings:
        #         # update the recipe's average rating
        #         value['avg_rating'] = recipe_ratings[recipe_id]

        return render(request, 'results.html', context={
            'results': recipes,
            'ingredients': ingredients.title(),
            'message': message
            })
    

def recipe(request, recipe_id):
    if request.user.id:
        user = User.objects.get(pk=request.user.id)
    else:
        user = False

    # if recipe is already saved in database get the data from the db
    if Recipe.objects.filter(spoonacular_id=recipe_id).exists():
        recipe = Recipe.objects.get(spoonacular_id=recipe_id)

    elif Recipe.objects.filter(pk=recipe_id).exists():
        recipe = Recipe.objects.get(pk=recipe_id)

    else:
        # get recipe details
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        data = get_recipes(url, recipe_id)
        fields = RECIPE_DATA_FIELDS['recipe_details']
        recipe_data = unpack_recipe_data(data, **fields)
        # save recipe to database
        recipe = Recipe.objects.create(spoonacular_id=recipe_id, 
                                        title=recipe_data['title'],
                                        )
                    
        # save recipe details to database
        recipe_details = RecipeDetails.objects.create(recipe=recipe,
                                                    ingredients=recipe_data['ingredients'],
                                                    instructions=recipe_data['instructions'],
                                                    description=recipe_data['summary'],
                                                    cooking_time=recipe_data['cooking_time'],
                                                    image=recipe_data['image'],
                                                    servings=recipe_data['servings'],
                                                    )
        # save recipe's dietary tags to database
        recipe_dietary_tags = RecipeDietaryTags.objects.create(recipe=recipe,
                                                                vegetarian=recipe_data['is_vegetarian'],
                                                                vegan=recipe_data['is_vegan'],
                                                                dairy_free=recipe_data['is_dairy_free'],
                                                                gluten_free=recipe_data['is_gluten_free'],
                                                                )
        recipe = Recipe.objects.get(spoonacular_id=recipe_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        # handle saving the recipe
        if 'status' in data:
            is_saved = data.get('status')
            if is_saved == 'false':
                user.saved_recipes.add(recipe.pk)
            elif is_saved == 'true':
                user.saved_recipes.remove(recipe.pk)
            return HttpResponse()
        
        # handle rating the recipe
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
        if user.saved_recipes.filter(id=recipe.pk).exists():
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
    # recipe_data['top_recipes'] = Recipe.getTopRecipes(num=3)
    # recipe_data['recent_recipes'] = Recipe.getRecentRecipes(num=3)
    return render(request, 'view_recipe.html', context={
        'recipe': recipe,
        'recipe_saved': recipe_saved,
        'user_rating': user_rating,
        'avg_rating': avg_rating['rating__avg']

    })


def new_recipe(request):
    if request.method == 'POST':
        form = NewRecipe(request.POST, request.FILES)
        if form.is_valid():

            # get form data
            title = request.POST.get('title')
            description = form.cleaned_data['description']
            image = form.cleaned_data['upload_image']
            servings = form.cleaned_data['servings']
            cooking_time = form.cleaned_data['cooking_time']
            
            # Get instructions
            instructions = request.POST.getlist('recipe-instructions')

            # Get ingredients
            ingredients = request.POST.getlist('recipe-ingredients')

            # Get current user
            user_instance = User.objects.get(pk=request.user.id)

            recipe = Recipe.objects.create(
                created_by=user_instance,
                title=title,
            )
            recipe_instance = Recipe.objects.get(pk=recipe.pk)
            RecipeDetails.objects.create(
                recipe=recipe_instance,
                ingredients=ingredients,
                instructions=instructions,
                description=description,
                cooking_time=cooking_time,
                servings=servings,
                upload_image=image,
            )

            return redirect('recipe', recipe.pk)
        else:
            print(form.errors)
    form = NewRecipe()
    return render(request, 
                  'new_recipe.html', 
                  context={
                      'form': form})


def user(request, id):
    recipes_saved = Recipe.objects.filter(users_who_saved=id)
    user_recipes = Recipe.objects.filter(created_by=id)
    user = User.objects.get(pk=id)
    return render(request, 
                  'user.html',      
                  context={
                    'profile': user,
                    'recipes': recipes_saved,
                    'user_recipes': user_recipes
                    })


def browse(request):
    recipes = Recipe.objects.all()
    
    return render(request, 
                  'browse.html', 
                  context={
                      'recipes': recipes
                  })