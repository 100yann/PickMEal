document.addEventListener("DOMContentLoaded", () => {
    var numInstructions = 1
    const addInstructions = document.getElementById('add-instruction')
    addInstructions.onclick = ((event) => {
        event.preventDefault()
        numInstructions++

        const orderedList = document.getElementById('instructions')
        const newStep = document.createElement('li')
        newStep.innerHTML = '<input class="form-control" type="text">'
        orderedList.insertBefore(newStep, orderedList.lastChild)

        if (numInstructions > 1){
            const removeStep = document.getElementById('remove-instruction')
            removeStep.style.display = 'inline-block'
            removeStep.onclick = ((event) => {
                event.preventDefault()
                numInstructions--;
                if (numInstructions === 1){
                    removeStep.style.display = 'none'
                }
            })
        }




    })
})