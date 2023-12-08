from .models import Recipe, RecipeDetails, RecipeDietaryTags
from django.conf import settings
import requests
import re


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
        elif response.status_code == 402:
            return False

    
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
    return set(ing['original'].capitalize() for ing in ingredients)


def save_api_recipe_to_db(recipe_id):
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
    RecipeDetails.objects.create(recipe=recipe,
                                ingredients=recipe_data['ingredients'],
                                instructions=recipe_data['instructions'],
                                description=recipe_data['summary'],
                                cooking_time=recipe_data['cooking_time'],
                                image=recipe_data['image'],
                                servings=recipe_data['servings'],
                                )
    # save recipe's dietary tags to database
    RecipeDietaryTags.objects.create(recipe=recipe,
                                    vegetarian=recipe_data['is_vegetarian'],
                                    vegan=recipe_data['is_vegan'],
                                    dairy_free=recipe_data['is_dairy_free'],
                                    gluten_free=recipe_data['is_gluten_free'],
                                    )


def search_user_recipes(ings, dietary_tags=None):

    results = {}
    ings = ings.split(',')
    for ing in ings:
        matching_recipes = RecipeDetails.objects.filter(ingredients__contains=ing)

        if dietary_tags:
            for match in matching_recipes:
                recipe = match.recipe
                recipe_dietary_tags = RecipeDietaryTags.objects.filter(recipe=recipe).first()
                if recipe_dietary_tags and recipe_dietary_tags.check_matching_tags(dietary_tags):
                    results[match] = results.get(match, []) + [ing]

        else:
            for match in matching_recipes:
                results[match] = results.get(match, []) + [ing]
    
    return results

def ingredients_to_list(ings):
    if ings[0] == "{" or ings[0] == "[":
        inside_braces = ings[1:-1]
    else:
        inside_braces = ings
    # Split by commas outside of quotes
    split_elements = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", inside_braces)

    # Remove extra spaces and quotes
    ingredient_list = [element.strip(" '") for element in split_elements]

    return ingredient_list

def get_used_ings(ings_needed, ings_available):
    ings_needed_list = ingredients_to_list(ings_needed)
    ings_available_list = ings_available.split(', ')

    num_missing = len(ings_needed_list)
    num_used = 0
    used_ings = []
    for ing in ings_available_list:
        for needed_ing in ings_needed_list:
            if ing in needed_ing or ing.lower() in needed_ing or ing.title() in needed_ing:
                num_missing -= 1
                num_used += 1
                used_ings.append(ings_needed_list.pop(ings_needed_list.index(needed_ing)))
                
    return num_missing, num_used, used_ings, ings_needed_list
