document.addEventListener('DOMContentLoaded', () => {
    const buttonTopRated = document.getElementById('top-rated-btn')
    buttonTopRated.onclick = ((event) => {
        event.preventDefault()
        displayTopRated()
    })
})

function displayTopRated() {
    const recipesContainer = document.getElementById('saved-recipes');
    const recipes = Array.from(document.querySelectorAll('#recipe-card'));

    recipes.sort((a, b) => {
        const ratingA = parseFloat(a.querySelector('#rating')?.dataset.rating || 0);
        const ratingB = parseFloat(b.querySelector('#rating')?.dataset.rating || 0);
        return ratingB - ratingA;
    });

    recipes.forEach((recipe) => {
        recipesContainer.appendChild(recipe);
    });
}