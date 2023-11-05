window.addEventListener('DOMContentLoaded', () => {
    // get Rating Buttons
    const ratingButtons = document.querySelectorAll('.fa-burger')

    // If a user has already rated a recipe display their current rating
    if (userRating){

        ratingButtons.forEach((element, index) => {
            if (index <= userRating-1){
                element.classList.add('active')
            }
        })
    }

    const saveRecipeButton = document.getElementById('save-recipe')
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;    

    saveRecipeButton.onclick = (element => {
        let isSaved = saveRecipeButton.getAttribute('data-saved')
        saveRecipe(isSaved, csrfToken, saveRecipeButton)
    })

    ratingButtons.forEach((element, index1) => {
        element.onclick = () => {
            fetch('', {
                method: 'POST',
                body: JSON.stringify({
                    'rating': index1
                }),
                headers: {
                    'X-CSRFToken': csrfToken,
                }
            })
            ratingButtons.forEach((element, index2) => {
                if (index1 >= index2){
                    element.classList.add('active')
                } else {
                    element.classList.remove('active')
                }
            })
        }
    })  
})

function saveRecipe(isSaved, csrfToken, button){
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            'status': isSaved}),
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => {
        if (isSaved === 'false'){
            button.innerHTML = '<i class="fa-solid fa-bookmark fa-lg mr-3"></i>Recipe Saved'
            button.setAttribute('data-saved', 'true')
        } else {
            button.innerHTML = '<i class="fa-regular fa-bookmark fa-lg mr-3"></i>Save Recipe'
            button.setAttribute('data-saved', 'false') 
        }
    })
}
