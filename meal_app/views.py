from django.shortcuts import render, redirect, HttpResponse
import json
from .models import User, RegisterUser, Recipe, Rating, NewRecipe, RecipeDetails, RecipeDietaryTags
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg
from .utils import *





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
        recipe_ids = [recipes[key]['id'] for key in recipes.keys()]

        # Get recipies with the specified IDs and their ratings
        recipes_with_ratings = Recipe.objects.filter(spoonacular_id__in=recipe_ids).annotate(avg_rating=Avg('ratings__rating'))
        
        # Get ID and avg rating of each recipe object
        recipe_ratings = {recipe.spoonacular_id: recipe.avg_rating for recipe in recipes_with_ratings}
        
        # iterate through the returned recipes
        for key in recipes.keys():
            recipe_id = recipes[key]['id']
            if recipe_id in recipe_ratings:
                # update the recipe's average rating
                recipes[key]['avg_rating'] = recipe_ratings[recipe_id]

        # get recipes that are already stored in the website DB
        user_recipes = search_user_recipes(ingredients)
        for matching_recipe in user_recipes.keys():
            recipe_title = matching_recipe.recipe.title

            # check if the api has already returned this recipe
            if recipe_title not in recipes.keys():
                num_missing, num_used, list_used, list_missing = get_used_ings(
                    ings_needed=matching_recipe.ingredients, 
                    ings_available=ingredients)
                # update recipes that will be passed to results.html    
                recipes[recipe_title] = {
                    'id': matching_recipe.recipe.pk,
                    'num_used_ingredients': num_used,
                    'num_missing_ingredients': num_missing,
                    'missing_ings': list_missing,
                    'used_ings': list_used
                }
                if matching_recipe.recipe.created_by:
                    recipes[recipe_title]['image'] = matching_recipe.upload_image.url
                else:
                    recipes[recipe_title]['image'] = matching_recipe.image

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

    # check if it's a user recipe
    elif Recipe.objects.filter(pk=recipe_id).exists():
        recipe = Recipe.objects.get(pk=recipe_id)

    # if it doesn't exist save it to the db
    else:
        save_api_recipe_to_db(recipe_id)
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


    return render(request, 'view_recipe.html', context={
        'recipe': recipe,
        'recipe_saved': recipe_saved,
        'user_rating': user_rating,
        'avg_rating': avg_rating['rating__avg'],
        'top_recipes': Recipe.getTopRecipes(num=3),
        'recent_recipes': Recipe.getRecentRecipes(num=3)

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
            is_vegan = 'vegan' in request.POST
            is_vegetarian = 'vegetarian' in request.POST
            is_dairy_free = 'dairy-free' in request.POST
            is_gluten_free = 'gluten-free' in request.POST
            
            # Get instructions
            instructions = request.POST.getlist('recipe-instructions')

            # Get ingredients
            ingredients = request.POST.getlist('recipe-ingredients')
            ingredients_title = [ingredient.title() for ingredient in ingredients]
            ingredients_str = ', '.join(ingredients_title)
            # Get current user
            user_instance = User.objects.get(pk=request.user.id)

            recipe = Recipe.objects.create(
                created_by=user_instance,
                title=title,
            )
            recipe_instance = Recipe.objects.get(pk=recipe.pk)
            RecipeDetails.objects.create(
                recipe=recipe_instance,
                ingredients=ingredients_str,
                instructions=instructions,
                description=description,
                cooking_time=cooking_time,
                servings=servings,
                upload_image=image,
            )
            
            RecipeDietaryTags.objects.create(
                recipe=recipe_instance,
                vegetarian=is_vegetarian,
                vegan=is_vegan,
                dairy_free =is_dairy_free,
                gluten_free=is_gluten_free
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