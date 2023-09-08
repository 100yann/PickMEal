import requests
import sys
import os


def main():
    # Get a list of ingredients from the user.
    ingredients = user_ingredients()
    if not ingredients:
        sys.exit('No ingredients entered') 
        # Exit the program if no ingredients were provided.

    # Get recipes based on the user's ingredients.
    recipes = get_recipes(ingredients)
    if not recipes:
        sys.exit('''No results found. Please try again with different ingredients.''')
        # Exit if no recipes were found.

    # Initialize variables for recipe navigation.
    recipe_num = 0 
    run = True

    # Allow the user to browse recipes.
    while run:
        try:
            curr_recipe = recipes[recipe_num]

        except IndexError:
            sys.exit('\nWe\'re sorry, there are no more recipes found.')
        
        else:
            title, url, recipe_ingredients = get_recipe_details(curr_recipe)
            print('\n' + title)
            print('\nIngredients you need:')
            for i in recipe_ingredients:
                print('-', i)
            print('\nInstructions:', url)
            
        # Ask the user if they want to see another recipe.
        valid = False
        while not valid:
            retry = input('\nWould you like to see another recipe? Yes/No ').strip().lower()
            if retry == 'yes':
                os.system('cls')
                recipe_num += 1
                valid = True
                continue

            elif retry == 'no':
                sys.exit('\nWe\'re glad you liked the recipe. Bon Appetit!')
                # Exit if the user doesn't want to see more recipes.
            
            else:
                print('Invalid input')

      
# Function to get a list of ingredients from the user.
def user_ingredients():
    user_choice = input("Enter a list of ingredients you have:\n").lower().split(',')
    if user_choice != '':
        return user_choice
    return None


# Function to fetch recipes from the Edamam API based on user ingredients.
def get_recipes(ingredients):
    ingredients_as_str = ','.join(ingredients)
    params = {
        'type': 'public',
        'q': ingredients_as_str,
        'app_id': os.environ['edamam_app_id'], # Use Edamam API credentials stored in environment variables.
        'app_key': os.environ['edamam_app_key'],
    }

    response = requests.get('https://api.edamam.com/api/recipes/v2', params=params)
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', []) # Extract recipe data from the API response.
        return hits
    return None


# Function to print details of a recipe.
def get_recipe_details(recipe):
        try:
            label = recipe['recipe']['label']
            url = recipe['recipe']['url']
            recipe_ingredients = recipe['recipe']['ingredientLines']

        except IndexError:
            return None, None, None
            # Return None if there are no more recipes to display.
        
        else:
            return label, url, recipe_ingredients
            # Return the recipe details.



if __name__ == '__main__':
    main()