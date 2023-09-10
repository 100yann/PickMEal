import requests
import sys
import os
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import tempfile


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
            title, url, recipe_ingredients, img = get_recipe_details(curr_recipe)
            print('\n' + title)
            print('\nIngredients you need:')
            for i in recipe_ingredients:
                print('-', i)
            print('\nInstructions:', url)
            
        # Ask the user if they want to see another recipe.
            if yes_no_prompt('\nWould you like to see another recipe? Yes/No: '):
                os.system('cls')
                recipe_num += 1
                continue

            else:
                if yes_no_prompt('\nWould you like to save the recipe as a pdf? Yes/No: '):
                    export_pdf(title, url, img, recipe_ingredients)

                sys.exit('\nWe\'re glad you liked the recipe. Bon Appetit!')
                # Exit        


      
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
            img = recipe['recipe']['images']['REGULAR']['url']
        except IndexError:
            return None, None, None, None
            # Return None if there are no more recipes to display.
        
        else:
            return label, url, recipe_ingredients, img
            # Return the recipe details.

def yes_no_prompt(question):
    while True:
        user_response = input(question).strip().lower()
        if user_response == 'yes':
            return True
        elif user_response == 'no':
            return False
        else:
            print('Invalid input')


def export_pdf(recipe_title, url, img, ingredients):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=22)
    pdf.cell(190, 10, txt=recipe_title.title(), ln=2, align='C') # add title
    
    response = requests.get(img)
    image_data = response.content

    image = Image.open(BytesIO(image_data))
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        image.save(temp_file.name, 'JPEG')
        pdf.image(temp_file.name, x=100, y=30, w=100)
    
    pdf.set_font('Arial', size=14)
    pdf.multi_cell(80, 30, txt='Ingredients:', align='L')
    
    pdf.set_font('Arial', size=12)
    for ing in ingredients:
        pdf.multi_cell(80, 10, txt=f' - {ing}', align='L')

    pdf_name = recipe_title.replace(' ','_') + '_recipe.pdf'
    pdf.output(pdf_name)
    os.remove(temp_file.name)

if __name__ == '__main__':
    main()