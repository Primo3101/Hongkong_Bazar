document.addEventListener('DOMContentLoaded', function() {
    const profileDropdownLink = document.getElementById('profileDropdown');

    // Initialize Bootstrap dropdown with flip disabled (always aligns right)
    const profileDropdown = new bootstrap.Dropdown(profileDropdownLink, {
        popperConfig: {
            modifiers: [
                {
                    name: 'flip',
                    options: {
                        fallbackPlacements: [] // prevents flipping to left
                    }
                }
            ]
        }
    });

    // Show on hover
    profileDropdownLink.parentElement.addEventListener('mouseenter', function() {
        profileDropdown.show();
    });

    profileDropdownLink.parentElement.addEventListener('mouseleave', function() {
        profileDropdown.hide();
    });

    // Click still works, uses same alignment
});
