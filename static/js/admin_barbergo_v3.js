document.addEventListener("DOMContentLoaded", function() {
    // Bootstrap 5 / Jazzmin 3.0+ Dark Mode Override
    document.documentElement.setAttribute('data-bs-theme', 'light');
    document.body.setAttribute('data-bs-theme', 'light');
    document.body.classList.remove('dark-mode');
    
    // Sidebar override (Jazzmin forces data-bs-theme="dark" on sidebar sometimes)
    var sidebar = document.getElementById('jazzy-sidebar');
    if (sidebar) {
        sidebar.setAttribute('data-bs-theme', 'light');
    }
    
    var meta = document.createElement('meta');
    meta.name = "darkreader-lock";
    document.head.appendChild(meta);
    
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === "data-bs-theme") {
                if (document.documentElement.getAttribute('data-bs-theme') !== 'light') {
                    document.documentElement.setAttribute('data-bs-theme', 'light');
                }
                if (document.body.getAttribute('data-bs-theme') !== 'light') {
                    document.body.setAttribute('data-bs-theme', 'light');
                }
            }
        });
    });
    observer.observe(document.documentElement, {attributes: true});
    observer.observe(document.body, {attributes: true});
});
