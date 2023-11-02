from django.shortcuts import render, redirect
from django.conf import settings
from django.db import IntegrityError
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

        results = [{'title': item['title'], 
                    'image': item['image'], 
                    'missing_ings': [ingredient['name'] for ingredient in item['missedIngredients']]
                    } for item in recipes]
        
        return render(request, 'results.html', context={
            'results': results
            })
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