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
        if print_recipes(recipes, ingredients, recipe_num):
            # Ask the user if they want to see another recipe.
            retry = input('Would you like to see another recipe? yes/no').lower()
            if retry == 'yes':
                os.system('cls')
                recipe_num += 1
                continue
            elif retry == 'no':
                sys.exit('I\'m glad you liked the recipe. Bon Appetit!')
                 # Exit if the user doesn't want to see more recipes.
            else:
                os.system('cls')
                print('Invalid input, please retry')
        else:
            sys.exit('We\'re sorry, there are no more recipes found')
            # Exit if there are no more recipes to show.

      
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
def print_recipes(recipes, user_ing, n):
        try:
            label = recipes[n]['recipe']['label']
            url = recipes[n]['recipe']['url']
            recipe_ingredients = recipes[n]['recipe']['ingredientLines']

        except IndexError:
            return False 
            # Return False if there are no more recipes to display.
        
        else:
            have = []
            for i in user_ing:
                for phrase in recipe_ingredients:
                    if i in phrase:
                        # Add ingredients that the user has to the 'have' list.
                        have.append(phrase)
                        recipe_ingredients.remove(phrase)
                        # Remove those ingredients from the recipe list.
                    # i.replace("\\\\\\", '').replace('\\\\','')

            print("Ingredients you have:", have, sep='\n', end='\n\n')
            print("Ingredients you need:", recipe_ingredients, sep='\n', end='\n\n')
            return True
            # Return True to indicate that a recipe was successfully displayed.



if __name__ == '__main__':
    main()