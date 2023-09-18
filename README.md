# PickMEal
    #### Video Demo:  https://youtu.be/HWntg7E-5fM?si=T3WoANquzsY9uvh0)https://youtu.be/HWntg7E-5fM?si=T3WoANquzsY9uvh0
    #### Description: An ingredient-based recipe finder utilizing Edamam's API
    #### Libraries used: Requests, PyTest, Pillow, FPDF

How to use:
User's are prompted to enter a list of ingredients they have on hand, with which Edamam's API returns recipes matching the ingredients specified. 
The user can then browse through a number of recipes returned by the API, and when they like a recipe, they can export a PDF to save for future use.
The program does not accept invalid user input and supports Keyboard Interrupt quitting.
The program also has a 'random' feature where if the user inputs 'random' as an ingredient, the program will select a range of 1-5 random ingredients and use those for Edamam's API.
