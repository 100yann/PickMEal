import requests
import sys
import os
from fpdf import FPDF
from io import BytesIO
from PIL import Image
import tempfile
from pyfiglet import Figlet


def main():
    start()
    # Get a list of ingredients from the user.
    ingredients = user_ingredients()
    is_random = False
    if ingredients == "":
        sys.exit("No ingredients entered")
        # Exit the program if no ingredients were provided.

    elif ingredients == "random":
        random_ingredients = get_random()
        recipes = get_recipes(random_ingredients)
        is_random = True
    else:
        # Get recipes based on the user's ingredients.
        recipes = get_recipes(ingredients)

    if not recipes:
        sys.exit("""No results found. Please try again with different ingredients.""")
        # Exit if no recipes were found.

    # Initialize variables for recipe navigation.
    recipe_num = 0
    run = True

    # Allow the user to browse recipes.
    while run:
        curr_recipe = recipes[recipe_num]

        title, url, recipe_ingredients, img = get_recipe_details(curr_recipe)
        display_recipe(title, url, recipe_ingredients)
        # Ask the user if they want to see another recipe.
        if not is_random:
            if recipe_num == 0:
                user_prompt_recipes = yes_no_prompt(
                    "\nWould you like to see another recipe? Next/No: ",
                    valid_answers=["next", "no"],
                )
            elif recipe_num == len(recipes) - 1:
                user_prompt_recipes = yes_no_prompt(
                    "\nThis was the last recipe. Would you like to go back? Back/No: ",
                    valid_answers=["back", "no"],
                )
            else:
                user_prompt_recipes = yes_no_prompt(
                    "\nWould you like to see another recipe? Next/Back/No: ",
                    valid_answers=["next", "back", "no"],
                )

            if user_prompt_recipes == "next":
                recipe_num += 1
                os.system("cls")
                continue
            elif user_prompt_recipes == "back":
                recipe_num -= 1
                os.system("cls")
                continue

        user_prompt_pdf = yes_no_prompt(
            "\nWould you like to save the recipe as a pdf? Yes/No: ",
            valid_answers=["yes", "no"],
        )

        if user_prompt_pdf == "yes":
            export_pdf(title, url, img, recipe_ingredients)
            # Save the recipe as a pdf if user writes yes

        sys.exit("\nWe're glad you liked the recipe. Bon Appetit!")
        # Exit


def start():
    print("\nWelcome to")
    f = Figlet(font="big")
    print(f.renderText("PickMEal"))


# Function to get a list of ingredients from the user.
def user_ingredients():
    user_choice = input("Enter a list of ingredients you have:\n").lower()
    return user_choice


# Function to fetch recipes from the Edamam API based on user ingredients.
def get_recipes(ingredients):
    params = {
        "type": "public",
        "q": ingredients,
        "app_id": os.environ[
            "edamam_app_id"
        ],  # Use Edamam API credentials stored in environment variables.
        "app_key": os.environ["edamam_app_key"],
    }

    response = requests.get("https://api.edamam.com/api/recipes/v2", params=params)
    if response.status_code == 200:
        data = response.json()
        hits = data.get("hits", [])  # Extract recipe data from the API response.
        return hits
    return None


# Function to return details of a recipe.
def get_recipe_details(recipe):
    try:
        label = recipe["recipe"]["label"]
        url = recipe["recipe"]["url"]
        recipe_ingredients = recipe["recipe"]["ingredientLines"]
        img = recipe["recipe"]["images"]["REGULAR"]["url"]
    except (KeyError, TypeError) as e:
        return None, None, None, None
        # Return None if there are no more recipes to display.

    else:
        return label, url, recipe_ingredients, img
        # Return the recipe details.


def display_recipe(title, url, recipe_ingredients):
    print("\n" + "Dish: " + title)
    print("\nIngredients you need:")
    for i in recipe_ingredients:
        print("-", i)
    print("\nInstructions:", url)


def yes_no_prompt(question, valid_answers):
    while True:
        user_response = input(question).strip().lower()
        if user_response not in valid_answers:
            print("Invalid input")
        else:
            return user_response


def export_pdf(recipe_title, url, img, ingredients):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=22)
    pdf.cell(190, 10, txt=recipe_title.title(), ln=2, align="C")  # add title

    response = requests.get(img)
    image_data = response.content

    image = Image.open(BytesIO(image_data))
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        image.save(temp_file.name, "JPEG")
        pdf.image(temp_file.name, x=100, y=30, w=100)

    pdf.set_font("Arial", size=14)
    pdf.multi_cell(80, 30, txt="Ingredients:", align="L")

    pdf.set_font("Arial", size=12)
    for ing in ingredients:
        pdf.multi_cell(80, 5, txt=f" - {ing}", align="L")

    pdf.cell(190, 130, txt=f"Instructions: {url}", ln=1, align="C")
    forbidden_characters = ["/", "\\", "?", "%", "*", ":", "|", '"', "<", ">", ".", ","]

    pdf_name = recipe_title.lower()
    for i in forbidden_characters:
        pdf_name = pdf_name.replace(i, "")
    pdf_name = pdf_name.replace(" ", "_") + "_recipe.pdf"
    pdf.output(pdf_name)
    print(f"\nYour recipe was saved as {pdf_name} in {os.getcwd()}")
    os.remove(temp_file.name)


def get_random():
    import random

    num_of_ingredients = random.randint(1, 5)
    random_ingredients = []

    with open("random_ingredients.txt") as file:
        all_ingredients = file.readlines()
        for _ in range(num_of_ingredients):
            random_ingredients.append(random.choice(all_ingredients).strip())

    return random_ingredients


if __name__ == "__main__":
    # Check for the existence of environment variables
    if "edamam_app_id" not in os.environ or "edamam_app_key" not in os.environ:
        print(
            "Error: 'edamam_app_id' and 'edamam_app_key' environment variables are not set."
        )
        print(
            "Please set these environment variables with your Edamam API credentials."
        )
        exit(1)  # Exit the program with an error code
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram closed")
