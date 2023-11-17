var numInstructions = 1
var numIngredients = 1

document.addEventListener("DOMContentLoaded", () => {
    const recipeTitle = document.getElementById('id_title')
    const recipeDescr = document.getElementById('id_description')


    // Validate title length
    recipeTitle.addEventListener('keyup', () => {
        const displayTitleChars = document.getElementById('char-count-title')
        checkInput(recipeDescr, recipeTitle)
        calcInput(recipeTitle, displayTitleChars, 75)
    })

    // Validate description length 
    recipeDescr.addEventListener('keyup', () => {
        const displayDescrChars = document.getElementById('char-count-description')
        checkInput(recipeDescr, recipeTitle)
        calcInput(recipeDescr, displayDescrChars, 300)
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

// If title and description have values make the submit button active
function checkInput(element1, element2){
    if (element1.value.length > 0 && element2.value.length > 0){
        document.getElementById('save-new-recipe').disabled = false;
    } else {
        document.getElementById('save-new-recipe').disabled = true;
    }
}

// Check if a field has more than the maxChars inputted
function calcInput(elementToCheck, elementToDisplay, maxChars){
    const submitButton = document.getElementById('save-new-recipe')

    var charNums = elementToCheck.value.length
    elementToDisplay.textContent = `${charNums}/${maxChars}`;

    if (charNums > maxChars ){
        elementToCheck.style.border = '2px solid red'
        submitButton.disabled = true;
    } else if (charNums < maxChars) {
        elementToCheck.style.border = '1px solid rgb(206, 212, 218)'
    }
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