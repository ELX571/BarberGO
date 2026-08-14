document.addEventListener("DOMContentLoaded", () => {
    checkAuthState();
});

function checkAuthState() {
    const token = localStorage.getItem('access_token');
    const userDataRaw = localStorage.getItem('user_data');
    const authLinks = document.getElementById('authLinks');
    const addPostBtn = document.getElementById('addPostBtn');
    
    if (token) {
        // Handle Role Based Button Visibility
        if (userDataRaw) {
            try {
                const user = JSON.parse(userDataRaw);
                if (user.role === 'barber' && addPostBtn) {
                    addPostBtn.style.display = 'flex';
                }
            } catch(e) {}
        }

        // user is logged in
        authLinks.innerHTML = `
            <a href="/profile/" class="nav-brand" style="margin-right:1rem; font-size:1rem; color:var(--text-primary);">Profil</a>
            <button onclick="logout()" class="logout-link" style="background:none; border:none; cursor:pointer;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                Chiqish
            </button>
        `;
    } else {
        // User is not logged in
        authLinks.innerHTML = `
            <a href="/login/" class="login-link">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path><polyline points="10 17 15 12 10 7"></polyline><line x1="15" y1="12" x2="3" y2="12"></line></svg>
                Kirish
            </a>
        `;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login/';
}

// Helper to make API calls with JWT
async function apiCall(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (response.status === 401) {
        // Token might be expired. A real app would try to refresh here.
        // For now, just logout if unauthorized.
        logout();
    }

    return response;
}
