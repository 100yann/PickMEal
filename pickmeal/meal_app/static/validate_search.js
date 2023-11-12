document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('submit-search')
    searchButton.onclick = ((event) => {
        const ingredients = document.getElementById('recipe-search')
        if (ingredients.value === ''){
            ingredients.style.border = '2px solid red'
            ingredients.placeholder = 'This field cannot be empty!'
            ingredients.classList.add('recipe-search-error')
            event.preventDefault()
        }
    })
})