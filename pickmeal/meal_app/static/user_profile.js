document.addEventListener('DOMContentLoaded', () => {
    const showSavedRecipes = document.getElementById('show-saved')
    const showUserRecipes = document.getElementById('show-user')

    const savedRecipes = document.getElementById('saved-recipes')
    const userRecipes = document.getElementById('user-recipes')

    var numSavedRecipes = savedRecipes.childElementCount
    var numUserRecipes = userRecipes.childElementCount

    if (numSavedRecipes > numUserRecipes){
        userRecipes.style.display = 'none'
    } else if (numSavedRecipes < numUserRecipes || numSavedRecipes === numUserRecipes) {
        savedRecipes.style.display = 'none'
    } else {
        savedRecipes.parentElement.innerHTML += '<h3>No recipes added or saved yet.</h3>'
    }
    
    showSavedRecipes.onclick = (() => {
        console.log('asd')
         userRecipes.style.display = 'none'
         savedRecipes.style.display = 'grid'
    })

    showUserRecipes.onclick = (() => {
        userRecipes.style.display = 'grid'
        savedRecipes.style.display = 'none'
    })
})