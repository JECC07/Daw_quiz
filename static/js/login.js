document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameEmailInput = document.getElementById('username_email');
    const passwordInput = document.getElementById('password');

    form.addEventListener('submit', function(event) {
        // Prevent the form from submitting by default
        event.preventDefault();

        // Simple validation check
        const usernameEmail = usernameEmailInput.value.trim();
        const password = passwordInput.value.trim();

        if (usernameEmail === '' || password === '') {
            alert('Por favor, complete todos los campos.');
        } else {
            // If validation passes, submit the form
            form.submit();
        }
    });
});