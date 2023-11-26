document.addEventListener('DOMContentLoaded', () => {
    // Get the Filters select tag
    const selectFilter = document.getElementById('dietary-filters');

    // Add an event listener to detect changes
    selectFilter.onchange = (event) => {
        // Get the selected option's value
        var selectedFilterValue = event.target.value
        // Display recipes based on the filter selected
        displayByTag(selectedFilterValue)
    };

    // Get the Sort By select tag
    const selectSortBy = document.getElementById('sort-by')

    selectSortBy.onchange = (event) => {
        var selectedSortValue = event.target.value
        if (selectedSortValue === 'top-rated'){
            // display the top rated recipes first
            displayTopRated()
        } else if (selectedSortValue === 'recently-added'){
            // display the most recent recipes first
            displayByDate('descending')
        } else {
            // display the oldest recipe first (default behaviour)
            displayByDate('ascending')
        }
    }

    // Get the search bar
    const searchBar = document.getElementById('search-bar')
    console.log(searchBar)
    searchBar.onkeyup = (event) => {
        const recipesContainer = document.getElementById('saved-recipes');
        const recipes = Array.from(document.querySelectorAll('#recipe-card'));
        var searchValue = searchBar.value.toLowerCase()
        recipes.forEach((recipe) => {
            if (searchValue){
                const recipeTitle = recipe.querySelector('#recipe-title').textContent.toLowerCase()
                if (recipeTitle.includes(searchValue)){
                    if (recipe.hidden === true){
                        recipe.hidden = false;
                    }
                } else {
                    recipe.hidden = true;
                }
            } else {
                if (recipe.hidden === true){
                    recipe.hidden = false;
                }
            }
        })
    }  
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

function displayByDate(order) {
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
        if (order === 'ascending'){
            return addedOnA - addedOnB
        } else {
            return addedOnB - addedOnA
        }
    })

    recipes.forEach((recipe) => {
        recipesContainer.appendChild(recipe);
    })
}


function displayByTag(tag){
    const recipes = Array.from(document.querySelectorAll('#recipe-card'));
    recipes.forEach((recipe) => {
        if (tag === 'all'){
            recipe.hidden = false;
        } else {
            const recipeTag = recipe.querySelector(`#is-${tag}`)
            const recipeTagValue = recipeTag.dataset[tag]
    
            if (recipeTagValue === 'False' || !recipeTagValue){
                recipe.hidden = true;
            } else if (recipeTagValue && recipe.hidden === true){
                recipe.hidden = false;
            }
        }
    })
}