window.addEventListener('DOMContentLoaded', () => {
    // get Rating Buttons
    const ratingButtons = document.querySelectorAll('.fa-burger')
    const ratingParentDiv = document.querySelector('.rating')
    
    userRated(ratingButtons)

    ratingParentDiv.addEventListener('mouseleave', () => {
        ratingButtons.forEach((element) => {
            element.classList.remove('active')
            userRated(ratingButtons)
        })
    })

    // If a user has already rated a recipe display their current rating

    const saveRecipeButton = document.getElementById('save-recipe')
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;    

    saveRecipeButton.onclick = (element => {
        let isSaved = saveRecipeButton.getAttribute('data-saved')
        saveRecipe(isSaved, csrfToken, saveRecipeButton)
    })

    ratingButtons.forEach((element, index1) => {
        element.addEventListener('mouseover', () => {
            ratingButtons.forEach((element, index2) => {
                if (index2 <= index1){
                    element.classList.add('active')
                }
            })
        })
        element.addEventListener('mouseleave', () => {
            element.classList.remove('active')
        })

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
            userRating = index1+1
            userRated(ratingButtons)
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

function userRated(ratingButtons){
    if (userRating){

        ratingButtons.forEach((element, index) => {
            if (index <= userRating-1){
                element.classList.add('active')
            }
        })
    }

}