// JavaScript functions to handle the modal
function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}


// JavaScript functions to open and close the edit profile popup
function openEditProfilePopup() {
    document.getElementById("editProfilePopup").style.display = "block";
}

function closeEditProfilePopup() {
    document.getElementById("editProfilePopup").style.display = "none";
}




// Function to preview selected banner image
function previewBannerImage(input) {
    var bannerImagePreview = document.getElementById('banner-image-preview');

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            bannerImagePreview.style.display = 'block'; // Display the banner image preview
            bannerImagePreview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Function to preview selected profile image
function previewProfileImage(input) {
    var profileImagePreview = document.getElementById('profile-image-preview');

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            profileImagePreview.style.display = 'block'; // Display the profile image preview
            profileImagePreview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}


function showTab(tabName) {
    // Hide all tab content
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => {
        tab.style.display = 'none';
    });

    // Deactivate all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Show the selected tab content and activate the button
    document.getElementById(tabName).style.display = 'block';
    const activeButton = document.querySelector(`.tab-button[onclick="showTab('${tabName}')"]`);
    activeButton.classList.add('active');
}

// Initially show the "Posts" tab when the page loads
showTab('posts');




