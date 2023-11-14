var numInstructions = 1
var numIngredients = 1

document.addEventListener("DOMContentLoaded", () => {
    
    const addInstructions = document.getElementById('add-instruction')
    addInstructions.onclick = ((event) => {
        event.preventDefault()
        numInstructions++
        const orderedList = document.getElementById('instructions')
        const removeStep = document.getElementById('remove-instruction')

        addListElement(orderedList, 'instruction', removeStep, numInstructions)
    })

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