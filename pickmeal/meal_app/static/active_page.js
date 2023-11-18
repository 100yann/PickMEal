document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link')
    console.log(navLinks)
    const currentUrl = window.location.pathname
    console.log(currentUrl)
    navLinks.forEach((link) => {
        const linkUrl = link.getAttribute('data-url')

        if (currentUrl.includes(linkUrl)){
            link.classList.add('active')
        }
    })
})