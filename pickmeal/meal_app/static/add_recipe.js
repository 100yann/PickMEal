var numInstructions = 1
var numIngredients = 1

document.addEventListener("DOMContentLoaded", () => {
    const submitButton = document.getElementById('save-new-recipe')
    // Validate title
    const recipeTitle = document.getElementById('new-recipe-title')
    recipeTitle.addEventListener('keyup', () => {
        const chars = document.getElementById('keys-pressed')
        var charNums = recipeTitle.value.length
        chars.textContent = `keys pressed: ${charNums}/75`;
        if (charNums > 75){
            recipeTitle.style.border = '2px solid red'
            submitButton.disabled = true;
        } else {
            recipeTitle.style.border = '1px solid grey'
            recipeTitle.disabled = false;

        }
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