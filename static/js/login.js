document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginButton');

    // Function to handle role-based visibility
    function updateVisibility() {
        const userRole = sessionStorage.getItem('userRole');
        const addLink = document.getElementById('addLink');
        const updateLink = document.getElementById('updateLink');
        const deleteLink = document.getElementById('deleteLink');

        if (userRole === 'admin') {
            if (addLink) addLink.classList.remove('d-none');
            if (updateLink) updateLink.classList.remove('d-none');
            if (deleteLink) deleteLink.classList.remove('d-none');
        } else {
            if (addLink) addLink.classList.add('d-none');
            if (updateLink) updateLink.classList.add('d-none');
            if (deleteLink) deleteLink.classList.add('d-none');
        }
    }

    // Check visibility on page load
    updateVisibility();

    // Handle login form submission
    if (loginForm && loginButton) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const email = document.getElementById('userEmail').value;
            const password = document.getElementById('password').value;

            // Define the admin credentials
            const adminEmail = 'sohailaswedan45@gmail.com';
            const adminPassword = '12345678';

            if (email === adminEmail && password === adminPassword) {
                sessionStorage.setItem('userRole', 'admin');
                window.location.href = '/movies'; // Adjust to your actual route
            } else {
                sessionStorage.setItem('userRole', 'user');
                window.location.href = '/movies'; // Adjust to your actual route
            }
        });

        loginButton.addEventListener("click", function() {
            const email = document.getElementById('userEmail').value;
            localStorage.setItem("email", email);
        });
    }
});








