# PickMEal

### Video Demo
[Watch the video demo here](https://youtu.be/HWntg7E-5fM?si=T3WoANquzsY9uvh0)

### Description
PickMEal is an ingredient-based recipe finder that utilizes Edamam's API. It allows users to discover recipes based on the ingredients they have on hand. Users can also export their favorite recipes as PDFs for future use. The program is built using Python and relies on several libraries, including Requests, PyTest, Pillow, and FPDF.

### How to Use
1. **Enter Ingredients**: Users are prompted to enter a list of ingredients they currently have. 
   
2. **Recipe Search**: The program uses Edamam's API to fetch recipes that match the specified ingredients.

3. **Browse Recipes**: Users can browse through the list of recipes returned by the API to find one they like.

4. **Export as PDF**: When a user finds a recipe they want to save, they can export it as a PDF for future reference.

5. **Random Ingredient**: If the user inputs 'random' as an ingredient, the program will select a random range of 1-5 ingredients and use them for the Edamam's API search.

6. **Error Handling**: The program does not accept invalid user input and supports Keyboard Interrupt quitting.

### Libraries Used
- **Requests**: Used for making HTTP requests to Edamam's API.
- **PyTest**: Used for testing the program.
- **Pillow**: Used for image processing.
- **FPDF**: Used for creating PDFs.

### Environment Variables
Before running the program, please ensure you have set the following environment variables:

- edamam_app_id: Your Edamam API application ID.
- edamam_app_key: Your Edamam API application key.
  
### Issues
Unfortunately, Edamam's API lacks a direct "instructions" field within its JSON responses. As a result, the program must rely on providing a link to the original recipe website for cooking instructions. Additionally, the API occasionally fails to distinguish separating lines within the original recipes, leading to unexpected inclusions, such as "FOR THE TOMATOES," within the "ingredients" list. These limitations highlight the potential for future enhancements by considering alternative recipe-searching APIs that better align with the project's requirements.
