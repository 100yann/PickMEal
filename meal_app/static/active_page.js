document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link')
    const currentUrl = window.location.pathname
    navLinks.forEach((link) => {
        const linkUrl = link.getAttribute('data-url')

        if (currentUrl.includes(linkUrl)){
            link.classList.add('active')
        }
    })
})