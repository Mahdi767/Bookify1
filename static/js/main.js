document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // User Dropdown Menu Toggle
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenu = document.getElementById('user-menu');
    if (userMenuButton) {
        userMenuButton.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevents the window click event from firing immediately
            userMenu.classList.toggle('hidden');
        });
    }

    // Close dropdown when clicking outside
    window.addEventListener('click', (event) => {
        if (userMenu && !userMenu.classList.contains('hidden') && !userMenuButton.contains(event.target)) {
            userMenu.classList.add('hidden');
        }
    });
});