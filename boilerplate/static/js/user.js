/**
 * Validates the create-user-form and submits it if all fields are valid and password requirements are met
 * Uses HTML5 form validation and checks if the password validity flag is set to "true"
 */
function submitUserForm() {
    // Check if all required form fields are valid
    if (document.forms["create-user-form"].reportValidity()) {
        // Ensure the password meets all requirements before submitting
        if (document.getElementById("passed-validity").value === "true") {
            document.forms["create-user-form"].submit();
        }
    }
}

/**
 * Validates the update-user-form and submits it if valid
 * Allows form submission if password requirements are met or if both password fields are empty
 * @description This allows users to update their profile without changing their password
 */
function submitUserUpdate() {
    // Check if all required form fields are valid
    if (document.forms["update-user-form"].reportValidity()) {
        // Get references to the password input elements
        const passwordElement = document.getElementById("password");
        const passwordConfirmElement = document.getElementById("confirm-password");
        
        // Track whether password fields are empty
        let isPasswordFieldEmpty = true;
        let isPasswordConfirmFieldEmpty = true;
        
        // Check if the confirm password field has a value
        if ( passwordConfirmElement !== null && passwordConfirmElement.value > 0 ) {
            isPasswordConfirmFieldEmpty = false;
        }
        
        // Check if the password field has a value
        if ( passwordElement !== null && passwordElement.value > 0 ) {
            isPasswordFieldEmpty = false;
        }

        // Submit the form if password requirements are met OR both password fields are empty
        if ((document.getElementById("passed-validity").value === "true") || (isPasswordFieldEmpty && isPasswordConfirmFieldEmpty)){
            document.forms["update-user-form"].submit();
        }
    }
}

/**
 * Toggles the active status of a user by sending a POST request to the backend
 * Creates a temporary form and submits it to the toggle-active endpoint
 * @param {string} userUuid - The UUID of the user to toggle (activate/deactivate)
 */
function toggleUserActive(userUuid) {
    // Create a form element to submit the POST request
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/users/${userUuid}/toggle-active`;
    document.body.appendChild(form);
    form.submit();
}