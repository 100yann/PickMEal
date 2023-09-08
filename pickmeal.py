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
    '''
    while run:
        if print_recipes(recipes, ingredients, recipe_num):
            # Ask the user if they want to see another recipe.
            retry = input('\nWould you like to see another recipe? Yes/No ').strip().lower()
            if retry == 'yes':
                os.system('cls')
                recipe_num += 1
                continue
            elif retry == 'no':
                sys.exit('\nWe\'re glad you liked the recipe. Bon Appetit!')
                 # Exit if the user doesn't want to see more recipes.
        else:
            sys.exit('We\'re sorry, there are no more recipes found')
            # Exit if there are no more recipes to show.
    '''
      
# Function to get a list of ingredients from the user.
def user_ingredients():
    user_choice = input("Enter a list of ingredients you have:\n").lower().split(',')
    if user_choice != '':
        return user_choice
    return None


# Function to fetch recipes from the Edamam API based on user ingredients.
def get_recipes(ingredients):
    params = {
        'apiKey': os.environ['spoon_key'],
        'ingredients': ingredients,
        'number': 5,
        'instructionsRequired': True,
    }

    response = requests.get('https://api.spoonacular.com/recipes/complexSearch', params=params)
    if response.status_code == 200:
        data = response.json()['results']
        return data
    return None


# Function to print details of a recipe.
def print_recipes(recipe, user_ing):
        try:
            title = recipe['title']
            url = recipe['recipe']['url']
        except IndexError:
            return False 
            # Return False if there are no more recipes to display.
        
        else:
            # print('', title, url, sep='\n')
            # print('\nIngredients you need:')
            # for i in recipe_ingredients:
            #     print('-', i)

            # print('\nFor instructions please visit the url.')
            return True
            # Return True to indicate that a recipe was successfully displayed.



if __name__ == '__main__':
    main()