document.addEventListener('DOMContentLoaded', function () {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));

            // Add active class to clicked link
            this.classList.add('active');

            // Get page name from data attribute
            const page = this.getAttribute('data-page');

            // Here you would typically load the page content
            // For Streamlit, we'll handle this differently
            console.log(`Navigating to ${page}`);
        });
    });

    // Emergency Modal
    const emergencyBtn = document.getElementById('emergency-btn');
    const modal = document.getElementById('emergency-modal');
    const closeBtn = document.querySelector('.close-btn');

    emergencyBtn.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Simulate loading different pages
    function loadPage(page) {
        // In a real implementation, this would fetch and display the correct content
        console.log(`Loading ${page} content`);
    }
});