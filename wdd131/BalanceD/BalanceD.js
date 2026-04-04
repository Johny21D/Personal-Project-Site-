// Burger Menu Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const burgerMenu = document.querySelector('.burger-menu');
    const navUl = document.querySelector('nav ul');

    if (burgerMenu && navUl) {
        burgerMenu.addEventListener('click', function() {
            const isExpanded = burgerMenu.getAttribute('aria-expanded') === 'true';
            burgerMenu.setAttribute('aria-expanded', !isExpanded);
            navUl.classList.toggle('open');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!burgerMenu.contains(e.target) && !navUl.contains(e.target)) {
                burgerMenu.setAttribute('aria-expanded', 'false');
                navUl.classList.remove('open');
            }
        });

        // Close menu when pressing Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && navUl.classList.contains('open')) {
                burgerMenu.setAttribute('aria-expanded', 'false');
                navUl.classList.remove('open');
            }
        });
    }
});