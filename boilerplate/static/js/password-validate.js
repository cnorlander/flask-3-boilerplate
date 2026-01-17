/**
 * Validates a password against configured requirements
 * Checks length, numeric, uppercase, lowercase, and special character requirements
 * Updates the password requirements list with violations and sets a validity flag
 * 
 * @param {number} passwordMinCharacters - Minimum required password length
 * @param {number} passwordMaxCharacters - Maximum required password length
 * @param {boolean} passwordRequireNumerals - Whether password must contain at least one number
 * @param {boolean} passwordRequireUpperCase - Whether password must contain at least one uppercase letter
 * @param {boolean} passwordRequireLowerCase - Whether password must contain at least one lowercase letter
 * @param {boolean} passwordRequireSpecialCharacters - Whether password must contain special characters
 * @param {string} passwordListOfAllowedSpecialCharacters - String containing allowed special characters
 * @returns {boolean} True if password meets all requirements, false otherwise
 */
function validatePassword(passwordMinCharacters, passwordMaxCharacters, passwordRequireNumerals, passwordRequireUpperCase, passwordRequireLowerCase, passwordRequireSpecialCharacters, passwordListOfAllowedSpecialCharacters) {
    // Array to store all broken password requirements
    let passwordRulesBroken = [];
    let passwordRulesBrokenHTML = ""
    
    // Get the password values from the form inputs
    const newPassword = document.getElementById("password").value
    const confirmPassword = document.getElementById("confirm-password").value
    
    // Get the requirements list element to update
    const passwordRequirementsList = document.getElementById("password-requirements")

    // Check minimum password length
    if (newPassword.length < passwordMinCharacters) {
        passwordRulesBroken.push(`Password is too short. Passwords should contain at least ${passwordMinCharacters} characters.`);
    }

    // Check maximum password length
    if (newPassword.length > passwordMaxCharacters) {
        passwordRulesBroken.push(`Password is too long. Passwords should contain at most ${passwordMaxCharacters} characters.`);
    }

    // Check for required numerals if configured
    if (passwordRequireNumerals && (!/\d/.test(newPassword))) {
        passwordRulesBroken.push(`Password must contain at least one number.`);
    }

    // Check for required uppercase letters if configured
    if (passwordRequireUpperCase && (!/[A-Z]/.test(newPassword))) {
        passwordRulesBroken.push(`Password must contain at least one upper case letter.`);
    }

    // Check for required lowercase letters if configured
    if (passwordRequireLowerCase && (!/[a-z]/.test(newPassword))) {
        passwordRulesBroken.push(`Password must contain at least one lower case letter.`);
    }

    // Check for required special characters if configured
    if (passwordRequireSpecialCharacters && (!newPassword.match(new RegExp(`[${passwordListOfAllowedSpecialCharacters}]`)))) {
        passwordRulesBroken.push(`Password must contain at least one special symbol of the following: ${passwordListOfAllowedSpecialCharacters}`);
    }

    // Check if passwords match
    if (newPassword !== confirmPassword) {
        passwordRulesBroken.push(`Password does not match the confirmed password.`);
    }

    // Build HTML for displaying broken requirements as a list
    for (const brokenRequirement of passwordRulesBroken) {
        passwordRulesBrokenHTML = passwordRulesBrokenHTML + `<li class="text-danger">${brokenRequirement}</li>`
    }
    
    // Update the requirements list with broken requirements (displayed in red)
    passwordRequirementsList.innerHTML = passwordRulesBrokenHTML;

    // Set the validity flag and return success if no requirements are broken
    if (passwordRulesBroken.length === 0){
        document.getElementById("passed-validity").value = "true"
        return true;
    }
    
    // Set the validity flag to false and return failure if requirements are broken
    document.getElementById("passed-validity").value = "false"
    return false
}
