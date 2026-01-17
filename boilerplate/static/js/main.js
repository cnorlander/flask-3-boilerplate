// Initialize document event listeners when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function (event) {
    // Attach click and touch event listeners to the document to handle sidenav closing
    document.addEventListener('click', handleClickEvent);
    document.addEventListener('touchstart', handleClickEvent);

    /**
     * Handles click and touch events to close the sidenav when clicking outside of it
     * Checks if the page has the #sidenav-open hash and if the click target is outside the nav element
     * If both conditions are true, triggers the sidenav close button
     * @param {Event} event - The click or touch event
     */
    function handleClickEvent(event) {
        var nav = document.querySelector('nav');
        var isNavOpen = window.location.hash == '#sidenav-open';
        var isDescendant = nav.contains(event.target);

        // Close sidenav if it's open and the user clicked outside of the nav element
        if (!isDescendant && isNavOpen) {
            document.getElementById("sidenav-close").click()
        }
    }
});

/**
 * Filters table rows based on a search word
 * Hides rows that don't contain the search term and shows rows that do
 * @param {string} parentId - The ID of the table element to filter
 * @param {string} filterItem - The HTML tag name to filter (e.g., 'tr' for table rows)
 * @param {string} word - The search term to filter by
 */
function filter(parentId, filterItem, word) {
    const table = document.getElementById(parentId);
    const rows = table.getElementsByTagName(filterItem);
    for (let i = 1; i < rows.length; i++) {
        const rowText = rows[i].textContent.toLowerCase();
        if (!rowText.includes(word.toLowerCase())) {
            rows[i].style.display = 'none';
        } else {
            rows[i].style.display = '';
        }
    }
}

// Global variable to track the initial visibility state
let initialState = true;

/**
 * Toggles the visibility of elements with classes "initial-shown" and "initial-hidden"
 * When toggled, hides initially shown elements and shows initially hidden elements, and vice versa
 * Uses Bootstrap's "d-none" class to control visibility
 */
function toggleInitialVisability() {
    // Get all elements that should be initially shown
    initiallyShownElements = document.querySelectorAll(".initial-shown")
    // Get all elements that should be initially hidden
    initiallyHiddenElements = document.querySelectorAll(".initial-hidden")
    
    // Toggle the "d-none" class on initially shown elements
    for (const element of initiallyShownElements) {
        if (initialState) element.classList.add("d-none")
        else element.classList.remove("d-none")
    }
    
    // Toggle the "d-none" class on initially hidden elements
    for (const element of initiallyHiddenElements) {
        if (initialState) element.classList.remove("d-none")
        else element.classList.add("d-none")
    }
    
    // Toggle the initial state for next time this function is called
    initialState = !initialState;
}
