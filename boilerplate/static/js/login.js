/**
 * Populates the email confirmation field with the value from the email input field
 * Used on the login page to ensure the confirmation email matches the entered email
 */
function populateEmail() {
    // Set the confirmation email field value to match the primary email field value
    document.querySelector("#email-confirm").value = document.querySelector("#email").value
}
