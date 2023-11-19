document.addEventListener('DOMContentLoaded', () => {
    // filter by top rated recipes
    const buttonTopRated = document.getElementById('top-rated-btn')
    buttonTopRated.onclick = ((event) => {
        event.preventDefault()
        displayTopRated()
    })

    // filter by recently added recipes
    const buttonRecentlyAdded = document.getElementById('recently-added-btn')
    buttonRecentlyAdded.onclick = ((event) => {
        event.preventDefault()
        displayRecentlyAdded()
    })

    // show only vegan recipes
    const buttonVegan = document.getElementById('vegan')
    buttonVegan.onclick = ((event) => {
        event.preventDefault()
        displayByTag('vegan')
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
        if (recipe.hidden){
            recipe.hidden = false;
        }
        recipesContainer.appendChild(recipe);
    });
}

function displayRecentlyAdded() {
    const recipesContainer = document.getElementById('saved-recipes');
    const recipes = Array.from(document.querySelectorAll('#recipe-card'));

    recipes.sort((a, b) => {
        const addedOnA = new Date(a.querySelector('#added-on')?.dataset.addedOn);
        const addedOnB = new Date(b.querySelector('#added-on')?.dataset.addedOn);

        // Check if the date is valid
        if (isNaN(addedOnA) || isNaN(addedOnB)) {
            console.error('Invalid date string in dataset.addedOn:', a.querySelector('#added-on')?.dataset.addedOn);
            return 0; // If invalid, treat as equal
        }

        return addedOnB - addedOnA;
    });

    recipes.forEach((recipe) => {
        if (recipe.hidden){
            recipe.hidden = false;
        }
        recipesContainer.appendChild(recipe);
    });
}


function displayByTag(tag){
    const recipesContainer = document.getElementById('saved-recipes');
    const recipes = Array.from(document.querySelectorAll('#recipe-card'));
    recipes.forEach((recipe) => {
        const recipeTag = recipe.querySelector(`#is-${tag}`)
        const recipeTagValue = recipeTag.dataset[tag]

        if (!recipeTagValue){
            recipe.hidden = true;
        }
    })
}