# PickMeal

## Video Demo
[Watch the video demo here](https://youtu.be/H1MHcK6FtnA)

## Description
PickMeal is an ingredient-based recipe finder that allows users to discover recipes based on the ingredients they have on hand, as well as filter by dietary preferences. It utilizes Spoonacular's API to search for recipes, which are later saved in the database to avoid excessive API requests. The website is built using Python, Django, and Javascript.

## Features
- [x] **Register and Login**
- [x] **Search for recipes by ingredients**
- [x] **Search for recipes by ingredients and dietary preferences**
- [x] **Browse recipes and filter by dietary preferences or sort by top-rated recipes**
- [x] **Rate recipes**
- [x] **Save recipes for easier access**
- [x] **User profile**
- [x] **Create new recipes**

## Distinctiveness and Complexity

### Distinctiveness
1. **Integrated Functionality:**
   - The website manages both Spoonacular API response data and also allows users to create new recipes.

2. **Advanced Database Queries:**
   - Handled more complex database queries, including calculations for top-rated recipes and matching dietary preferences.

3. **User-Friendly Interface:**
   - Implemented features like a search bar, filters, and sorting options for enhanced user navigation and experience.

4. **Mobile Responsiveness**

### Complexity
It was challenging to integrate the different API endpoints of Spoonacular. Each endpoint — whether it involved searching by ingredients, accessing a specific recipe, or combining ingredients with dietary preferences — had its distinct URL and returned varying amounts of data. I was able to optimize this by creating the 'get_recipes' function accepts the API endpoint as a parameter, as well as keyword arguments representing the API parameters. Additionally, the 'unpack_recipe_data' function handled the diverse JSON responses from Spoonacular.

I was able to handle complex database queries by creating model class functions that helped me keep my code clean and straightforward - sorting class methods like 'getRecentRecipes', 'getTopRecipes', as well as 'check_matching_tags' which checked if a recipe's dietary tags match a user's query.

It was also interesting to create client-side validation when creating a new recipe that:
- Checked whether all fields were filled in
- Checked if Title and Description didn't exceed the character limit
- Dynamic addition of more fields for ingredients and instructions.

## Project Structure

### meal_app
Contains the primary functionality of the website.

- **views.py**:
- 'new_recipe': Handles form data for creating new recipes, combining model forms and HTML forms.
- 'results': Displays matching recipes from Spoonacular's API and the website's database.
- 'recipe': Displays details of a specific recipe, as well as checking if the user has saved or rated it.

- **utils.py**:
- 'get_recipes': An all-purpose function designed to fetch data from Spoonacular's multiple API endpoints using kwargs.
- 'unpack_recipe_data': Unpacks necessary data from the different JSON response objects from Spoonacular's API.
- 'search_user_recipes': Searches the database for matching recipes based on ingredients and dietary preferences.

- **urls.py**:
- Handles the mapping between URLs and Django views.

- **models.py**:
- 'User': A standard user model with a ManyToMany field for saved recipes.
- 'Recipe': Main recipe model for the id, title, date of creation, and author.
- 'RecipeDetails': Contains all details about a recipe like the ingredients, instructions, description, cooking time, servings, image, etc.
- 'RecipeDietaryTags': Contails a recipe's dietary tags and the check_matching_tags function to check if a recipe matches a user's search criteria.
- 'Rating': Contains the recipe, rating, and the user who rated it.
- 'RegisterUser' and 'NewRecipe' - Model Forms for creating a new user or recipe.

- **static**:
- 'active-page.js': Updates the active Navbar button based on the current URL, providing a visual indication of the active page.
- 'add_recipe.js': Client-side validation for creating a new recipe.
- 'filters.js': Manages the functionality of the search bar, filters and order-by options on the Browse page.
- 'user_profile.js': Toggle between displaying user-created recipes or saved recipes.
- 'validate_search.js': Validates the search field on the Home page. Redirects users to the advanced search page and prepoluates the search field there with the value of the search bar on the home page.
- 'view-recipe.js': Handle saving and rating a specific recipe.
- 'styles.css': Contains all styling CSS code for the website.

-**templates**:
- 'advanced_search.html': Contains advanced search functionality with input fields for ingredients, maximum preparation time, and dietary preference switches.
- 'browse.html': Displays all recipes in the website's database as well as a search bar, filters and order-by options to help users find what they're looking for. 
- 'index.html': Home page of the website. Allows users to search by ingredients and contains a button to redirect users to Advanced Search.
- 'layout.html': HTML template that contains Bootstrap CDN, CSS, Navbar.
- 'new_recipe.html': Allows users to create a new recipe by combining Django ModelForms and HTML forms.
- 'register.html': Page for new users to register.
- 'results.html': Displays all recipes returned by Spoonacular's API and the database that match the user's search criteria.
- 'sign_in.html': Page for users to sign in.
- 'top_recipes.html': Display the 3 top rated recipes and 3 recently added recipes. Used in view_recipe.html when viewing on a big screen.
- 'user.html': User Profile Page that displays a user's saved and created recipes. Used as your own personal cookbook where you can store recipes.
- 'view_recipe.html': Displays detailed information about a specific recipe, including buttons for logged-in users to rate and save the recipe.

- **mediafiles\recipe_images**:
- Contains the images for user-created recipes.

## How to Run 
1. **Clone**: Run git clone https://github.com/100yann/PickMEal.git in the terminal to clone the repository
2. **Set up environment variable**: To use the website locally, you'd need to enter your own SPOONACULAR_API key as an environment variable
3. **Install Dependencies**: Install the required libraries by running pip install -r requirements.txt
4. **Make and apply migrations**: Run 'python3 manage.py makemigrations'. Afterwards run 'python3 manage.py migrate'
5. **Run the server**: Run python3 manage.py runserver to start the server

## Libraries Used
- **Requests**: Used for making HTTP requests to Spoonacular's API.
- **Pillow**: Used for image processing.
- **Django**: Used as the back-end.

## Error handling
- **Registration and Sign In**: Server-side validation with Django
- **Searching For and Creating Recipes**: Client-side validation with JavaScript
