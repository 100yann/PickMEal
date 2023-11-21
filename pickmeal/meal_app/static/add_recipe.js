var numInstructions = 1
var numIngredients = 1

document.addEventListener("DOMContentLoaded", () => {


    const recipeTitle = document.getElementById('id_title')
    const recipeDescr = document.getElementById('id_description')
    
    const recipeForm = document.getElementById('recipe-form')
    // check if all fields are filled in. If true the submit button will be active
    recipeForm.addEventListener('input', () => {
        checkInput(recipeTitle, recipeDescr)});


    // Validate title length
    recipeTitle.addEventListener('keyup', () => {
        const displayTitleChars = document.getElementById('char-count-title')
        displayAmountOfCharacters(recipeTitle, displayTitleChars, 75)
    })

    // Validate description length 
    recipeDescr.addEventListener('keyup', () => {
        const displayDescrChars = document.getElementById('char-count-description')
        displayAmountOfCharacters(recipeDescr, displayDescrChars, 1000)
    })

    // Add new instruction step field
    const addInstructions = document.getElementById('add-instruction')
    addInstructions.onclick = ((event) => {
        event.preventDefault()
        numInstructions++
        const orderedList = document.getElementById('instructions')
        const removeStep = document.getElementById('remove-instruction')

        addListElement(orderedList, 'instruction', removeStep, numInstructions)
    })

    // Add new ingredient field
    const addIngredients = document.getElementById('add-ingredient')
    addIngredients.onclick = ((event) => {
        event.preventDefault()
        numIngredients++
        const ingsOrderedList = document.getElementById('ingredients')
        const removeStep = document.getElementById('remove-ingredient')

        addListElement(ingsOrderedList, 'ingredient', removeStep, numIngredients)
    })
})

// Check if all fields are filled
function checkInput(recipeTitle, recipeDescr){

    // By default tje submit button is active
    const submitButton = document.getElementById('save-new-recipe')
    submitButton.disabled = false;

    const titleValue = recipeTitle.value
    const descriptionValue = recipeDescr.value
    const instructionsValue = document.getElementById('recipe-instructions').value
    const ingredientsValue = document.getElementById('recipe-ingredients').value
    const servingsValue = document.getElementById('id_servings').value
    const cookingTimeValue = document.getElementById('id_cooking_time').value
    const recipeImage = document.getElementById('id_upload_image').value
    const validateFields = [titleValue, descriptionValue, instructionsValue, ingredientsValue, servingsValue, cookingTimeValue, recipeImage]
    console.log(servingsValue)
    // if there's an empty field disable the button
    validateFields.some(element => {
        if (element === ''){
            submitButton.disabled = true;
        }
        if (servingsValue < 0 || cookingTimeValue < 0){
            submitButton.disabled = true;
        }

        // Check title length
        if (titleValue.length > 75){
            recipeTitle.style.border = '2px solid red'
            submitButton.disabled = true;
        } else if (titleValue.length < 75) {
            recipeTitle.style.border = '1px solid rgb(206, 212, 218)'
        }

        // Check description length
        if (descriptionValue.length > 1000){
            recipeDescr.style.border = '2px solid red'
            submitButton.disabled = true;
        } else if (descriptionValue.length < 1000){
            recipeDescr.style.border = '1px solid rgb(206, 212, 218)'
        }
    })
}

// Display the amount of chars inputted in title and description
function displayAmountOfCharacters(elementToCheck, elementToDisplay, maxChars){
    var charNums = elementToCheck.value.length
    elementToDisplay.textContent = `${charNums}/${maxChars}`;

}

// Add a new list element to instructions/ingredients
function addListElement(parentElement, buttonName, removeStep, num){
    const newStep = document.createElement('li')
    if (parentElement.id === 'instructions'){
        newStep.innerHTML = '<input class="form-control" type="text" name="recipe-instructions">'
    } else {
        newStep.innerHTML = '<input class="form-control" type="text" name="recipe-ingredients">'

    }
    
    parentElement.insertBefore(newStep, parentElement.lastChild)

    if (num > 1){
        removeStep.style.display = 'inline-block'
        removeStep.onclick = ((event) => {
            event.preventDefault()
            num--;
            if (buttonName === 'ingredient'){
                numIngredients--;
            } else {
                numInstructions--;
            }
            var lastLi = parentElement.lastElementChild
            parentElement.removeChild(lastLi)
            if (num === 1){
                removeStep.style.display = 'none'
            }
        })
    }

}