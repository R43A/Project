document.addEventListener("DOMContentLoaded", function () {
    const eyeIcon = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('inputPassword');

    if (eyeIcon && passwordInput) {
        eyeIcon.addEventListener('click', () => {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
            } else {
                passwordInput.type = 'password';
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    // Function to toggle the sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('active');
    }

    // Event listener to toggle the sidebar when the button is clicked
    sidebarToggle.addEventListener('click', toggleSidebar);

    // Event listener to close the sidebar when clicking outside of it
    document.addEventListener('click', function (event) {
        if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });

    // Prevent closing the sidebar when clicking inside it
    sidebar.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});



document.addEventListener("DOMContentLoaded", function() {
    var newsFeedMenuItem = document.getElementById("news-feed");

    if (newsFeedMenuItem) {
        newsFeedMenuItem.focus();
    }
    // Focus other links using their unique IDs if needed
});







