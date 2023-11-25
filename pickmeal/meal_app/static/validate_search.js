document.addEventListener('DOMContentLoaded', () => {
    const ingredients = sessionStorage.getItem('ingredients')
    if (ingredients){
        document.getElementById('advanced-recipe-search').value = ingredients
        sessionStorage.clear()
    }

    const searchButton = document.getElementById('submit-search')
    searchButton.onclick = ((event) => {
        validSearch(event)
    })
})

function validSearch(event){
    const ingredients = document.getElementById('recipe-search')
    if (ingredients.value === ''){
        ingredients.style.border = '2px solid red'
        ingredients.placeholder = 'This field cannot be empty!'
        ingredients.classList.add('recipe-search-error')
        event.preventDefault()
    }
}
// When advanced search is clicked the form is not submitted
// and instead the user is taken to an advanced search page
function advancedSearch(event){
    event.preventDefault()
    const currentSearch = document.getElementById('recipe-search').value
    window.location.href = '/advanced_search'
    sessionStorage.setItem('ingredients', currentSearch);
}