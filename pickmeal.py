import requests
import sys
import os
import json
import re

def main():
    ingredients = user_ingredients()
    if not ingredients:
        sys.exit('No ingredients entered')

    recipes = get_recipes(ingredients)
    if not recipes:
        sys.exit('''No results found. 
                 Please try again or try with different ingredients''')


    recipe_num = 0 
    run = True
    while run:
        if print_recipes(recipes, ingredients, recipe_num):
            retry = input('Would you like to see another recipe? yes/no').lower()
            if retry == 'yes':
                os.system('cls')
                recipe_num += 1
                continue
            elif retry == 'no':
                sys.exit('I\'m glad you liked the recipe. Bon Appetit!')
            else:
                os.system('cls')
                print('Invalid input, please retry')
        else:
            sys.exit('We\'re sorry, there are no more recipes found')



        

def user_ingredients():
    user_choice = input("Enter a list of ingredients you have:\n").lower().split(',')
    if user_choice != '':
        return user_choice
    return None

def get_recipes(ingredients):
    ingredients_as_str = ','.join(ingredients)
    params = {
        'type': 'public',
        'q': ingredients_as_str,
        'app_id': os.environ['edamam_app_id'],
        'app_key': os.environ['edamam_app_key'],
    }

    response = requests.get('https://api.edamam.com/api/recipes/v2', params=params)
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', [])
        return hits
    return None

def print_recipes(recipes, user_ing, n):
        try:
            label = recipes[n]['recipe']['label']
            url = recipes[n]['recipe']['label']
            recipe_ingredients = recipes[n]['recipe']['ingredientLines']

        except IndexError:
            return False
        
        else:
            have = []
            for i in user_ing:
                for phrase in recipe_ingredients:
                    if i in phrase:
                        have.append(phrase)
                        recipe_ingredients.remove(phrase)

                    i.replace("\\\\\\", '').replace('\\\\','')

            print("Ingredients you have:", have, sep='\n', end='\n\n')
            print("Ingredients you need:", recipe_ingredients, sep='\n', end='\n\n')
            return True




if __name__ == '__main__':
    main()