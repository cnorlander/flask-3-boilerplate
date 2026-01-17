/**
 * Adds visual flash effect to an element by adding and removing a CSS class
 * Used to indicate changes or selections to the user
 * 
 * @param {Element} textElement - The DOM element to flash
 */
function flash(textElement) {
    // Add the flashed class to trigger CSS animation
    textElement.classList.add("flashed");
    // Remove the flashed class after 100ms to allow the animation to play
    setTimeout(function () {
        textElement.classList.remove("flashed");
    }, 100);
}

/**
 * Creates reverse dependency tracking for permissions
 * If a permission requires other permissions, this tracks which permissions depend on it
 * Used to prevent unchecking a permission that is required by other checked permissions
 * 
 * @param {Element} item - The permission element to create reverse requirements for
 */
function createBackRequirements(item) {
    // Get the ID of the current permission
    const itemID = item.id;
    // Get the comma-separated list of required permissions from the data attribute
    const requires = item.getAttribute("data-requires");
    
    // If this permission requires other permissions
    if (requires != null) {
        // For each required permission
        for (const id of requires.replace(/ /g, '').split(",")) {
            // Find the required permission element
            requiredElement = document.getElementById(id);
            // Get any existing list of permissions that require this one
            existingValues = requiredElement.getAttribute("data-required-by");
            
            // Add this permission to the list of permissions that require the found permission
            if (existingValues == null || existingValues == "") {
                requiredElement.setAttribute("data-required-by", itemID);
            } else {
                requiredElement.setAttribute("data-required-by", existingValues + ", " + itemID);
            }
        }
    }
}

/**
 * Marks a checkbox as checked
 * Helper function used by the permission dependency system
 * 
 * @param {string} id - The ID of the checkbox to check
 */
function setChecked(id) {
    // Find the checkbox by ID and set its checked property to true
    checkbox = document.getElementById(id);
    checkbox.checked = true;
}

/**
 * Handles checkbox click events for permission dependencies
 * When a permission is unchecked, prevents unchecking if other permissions depend on it
 * When a permission is checked, automatically checks all required permissions
 * Recursively processes the dependency chain
 * 
 * @param {Element} target - The checkbox that was clicked
 * @param {Array} seen - Array to track already processed permissions (prevents infinite loops)
 */
function checkboxClicked(target, seen) {
    // Get the list of permissions that this one requires
    let requiredIDs = [];
    // Get the list of permissions that require this one
    let requiredByIDs = [];
    
    // Parse the data attributes to get dependency information
    const requiredByString = target.getAttribute("data-required-by");
    const requiredString = target.getAttribute("data-requires");
    
    if (requiredString != null && requiredString != "") {
        requiredIDs = requiredString.replace(/ /g, '').split(",");
    }
    if (requiredByString != null && requiredString != "") {
        requiredByIDs = requiredByString.replace(/ /g, '').split(",");
    }

    // If user is unchecking this permission and other permissions depend on it
    if (!target.checked && requiredByIDs.length > 0) {
        // For each permission that depends on this one
        for (const requiredByElementID of requiredByIDs) {
            // If a dependent permission is checked, re-check this permission and flash it
            if (document.getElementById(requiredByElementID).checked) {
                flash(document.getElementById(requiredByElementID).parentNode.parentNode.parentNode);
                setChecked(target.id);
            }
        }
    }

    // If user is checking this permission
    for (const requiredElementID of requiredIDs) {
        // Check all required permissions that haven't been processed yet
        if (target.checked && !seen.includes(requiredElementID)) {
            setChecked(requiredElementID);
            seen.push(requiredElementID);
            // Recursively check the required permission's dependencies
            checkboxClicked(document.getElementById(requiredElementID), seen);
        }
    }
}

/**
 * Creates click event listeners for permission checkboxes
 * Attaches the checkboxClicked handler to each checkbox
 * 
 * @param {Element} item - The checkbox element
 * @param {number} index - The index of the element (unused but provided by forEach)
 */
function createListeners(item, index) {
    // Add click event listener that calls checkboxClicked when the checkbox is clicked
    item.addEventListener("click", (event) => {
        checkboxClicked(event.target, []);
    });
}

/**
 * Unchecks all permission checkboxes
 * Used by the "Clear" or "Reset" button in the permissions UI
 */
function resetAllCheckboxes() {
    // Iterate through all checkboxes and uncheck them
    for (const checkbox of checkboxes) {
        checkbox.checked = false;
    }
}

/**
 * Checks all permission checkboxes
 * Used by the "Select All" button in the permissions UI
 */
function selectAllCheckboxes() {
    // Iterate through all checkboxes and check them
    for (const checkbox of checkboxes) {
        checkbox.checked = true;
    }
}

/**
 * Submits the permissions form after updating checkbox values
 * Converts checked checkboxes to "true" and unchecked to "false" for form submission
 */
function submitPermissionsForm() {
    // Get all checkboxes in the form
    const checkboxes = document.querySelectorAll("input[type=checkbox]");
    
    // Check if form passes HTML5 validation
    if (document.forms["permissions-form"].reportValidity()) {
        // For each checkbox, set its value based on whether it's checked
        for (const checkbox of checkboxes) {
            if (checkbox.checked) {
                checkbox.value = "true";
            } else {
                checkbox.value = "false";
            }
            // Note: This will submit the form for every checkbox - likely a bug, should be after the loop
            document.forms["permissions-form"].submit();
        }
    }
}

/**
 * Clears the role creation/edit modal to prepare for creating a new role
 * Resets all form fields and clears the header
 */
function clearModal() {
    // Set the modal header to "Create New Role"
    document.getElementById("create-edit-role-modal-header").innerHTML = "Create New Role";
    // Set the role ID to "new" to indicate this is a new role
    document.getElementById("role-id").value = "new";
    
    // Get all checkboxes and text inputs in the modal
    const checkboxes = document.querySelectorAll("input[type=checkbox]");
    const textboxes = document.querySelectorAll("input[type=text]");
    
    // Uncheck all checkboxes
    for (const checkbox of checkboxes) {
        checkbox.checked = false;
    }
    
    // Clear all text inputs
    for (const textbox of textboxes) {
        textbox.value = "";
    }
}

/**
 * Populates the role edit modal with existing role data
 * Used when the user clicks "Edit" on an existing role
 * 
 * @param {Object} role - The role object containing: uuid, name, description, hidden, system, actions
 */
function editRole(role) {
    // Clear the modal first to start fresh
    clearModal();
    
    // Set the modal header to show the role being edited
    document.getElementById("create-edit-role-modal-header").innerHTML = 'Editing Role "' + role.name + '"';
    // Set the role ID to the existing role's UUID
    document.getElementById("role-id").value = role.uuid;
    // Fill in the role name and description
    document.getElementById("role-name").value = role.name;
    document.getElementById("role-description").value = role.description;
    
    // Check the "hidden" checkbox if the role is hidden
    roleHiddenCheckbox = document.getElementById("role-hidden")
    if (roleHiddenCheckbox != null) {
        roleHiddenCheckbox.checked = role.hidden
    }
    
    // Check the "system" checkbox if the role is a system role
    roleSystemCheckbox = document.getElementById("role-system")
    if (roleSystemCheckbox != null) {
        roleSystemCheckbox.checked = role.system
    }

    // Check all permission checkboxes for actions assigned to this role
    for (const action of role.actions) {
        actionCheckbox = document.getElementById(action);
        if (actionCheckbox != null) {
            actionCheckbox.checked = true
        }
    }
}

/**
 * Populates the delete role confirmation modal
 * Sets up the modal to confirm deletion and show replacement role options if needed
 * 
 * @param {string} roleId - The UUID of the role being deleted
 * @param {string} roleName - The display name of the role being deleted
 * @param {number} roleCount - The number of users currently assigned to this role
 */
function deleteRole(roleId, roleName, roleCount) {
    // Clear the confirmation input field
    document.getElementById("delete-role-confirm").value = ""
    // Remove any validation error styling
    document.getElementById("delete-role-confirm").classList.remove("is-invalid")
    
    // Show replacement role info if there are users assigned to this role
    document.getElementById("replacement-info").style.display = "block";
    if (roleCount == 0) {
        document.getElementById("replacement-info").style.display = "none";
    }
    
    // Get all replacement role options
    const replacementRoleElements = document.getElementById("replacement-role-id").querySelectorAll("option");
    let setDefault = false;
    
    // Configure which roles can be selected as replacements
    for (const roleElement of replacementRoleElements) {
        roleElement.disabled = false;
        // Disable the role being deleted from replacement options
        if (roleElement.value == roleId) {
            console.log(roleElement.value, "==", roleId)
            roleElement.disabled = true
        } else if (!setDefault) {
            // Set the first available role as the default replacement
            setDefault = true;
            document.getElementById("replacement-role-id").value = roleElement.value;
        }
    }
    
    // Set the modal header and populate hidden fields
    document.getElementById("delete-role-modal-header").innerHTML = 'Delete Role "' + roleName + '"?';
    document.getElementById("disabled-role-name").value = roleName;
    document.getElementById("delete-role-id").value = roleId;
    document.getElementById("delete-role-count").value = roleCount;
}

/**
 * Confirms role deletion by verifying the user typed the role name
 * Submits the delete form if the typed name matches the role name being deleted
 */
function confirmDeleteRole() {
    // Check if the typed confirmation matches the role name
    if (document.getElementById("delete-role-confirm").value != document.getElementById("disabled-role-name").value) {
        // If not matching, add validation error styling
        document.getElementById("delete-role-confirm").classList.add("is-invalid")
    } else {
        // If matching, submit the delete form
        document.getElementById("delete-role-form").submit();
    }
}

// Initialize permission checkboxes when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function (event) {
    // Get all permission checkboxes in the dependent-checkboxes container
    const checkboxes = document.querySelectorAll(".dependent-checkboxes input[type=checkbox]");
    // Create event listeners for each checkbox
    checkboxes.forEach(createListeners);
    // Create reverse dependency tracking for each checkbox
    checkboxes.forEach(createBackRequirements);
});


