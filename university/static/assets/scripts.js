(function() {
    var menuToggle = document.getElementById("menu-toggle");
    var wrapper = document.getElementById("wrapper");
    var profilePic = document.getElementById("profile-pic");
    var profileMenu = document.getElementById("profile-menu");

    menuToggle.addEventListener("click", function() {
        wrapper.classList.toggle("toggled");
    });

    profilePic.addEventListener("mouseenter", function() {
        profileMenu.style.display = "block";
    });

    profilePic.addEventListener("mouseleave", function() {
        setTimeout(function() {
            if (!profileMenu.matches(":hover")) {
                profileMenu.style.display = "none";
            }
        }, 200);
    });

    profileMenu.addEventListener("mouseenter", function() {
        profileMenu.style.display = "block";
    });

    profileMenu.addEventListener("mouseleave", function() {
        profileMenu.style.display = "none";
    });

    // Function to toggle the visibility of content sections
    window.toggleElement = function(elementId) {
        var element = document.getElementById(elementId);
        if (element) {
            var sections = document.querySelectorAll(".content-section");
            sections.forEach(function(section) {
                section.style.display = "none";
            });
            element.style.display = "block";
        }
    }
})();
