document.addEventListener("DOMContentLoaded", () => {
    checkAuthState();
});

function checkAuthState() {
    const token = localStorage.getItem('access_token');
    const userDataRaw = localStorage.getItem('user_data');
    const authLinks = document.getElementById('authLinks');
    const addPostBtn = document.getElementById('addPostBtn');
    const currentPath = window.location.pathname;
    
    if (token) {
        // Redirect to home if user is already logged in but visits login/register
        if (currentPath === '/login/' || currentPath === '/register/') {
            window.location.href = '/';
            return;
        }

        // Handle Role Based Button Visibility
        if (userDataRaw) {
            try {
                const user = JSON.parse(userDataRaw);
                const userRole = (user.role || user.user_type || '').toLowerCase();
                
                if (userRole === 'barber') {
                    if (addPostBtn) addPostBtn.style.display = 'flex';
                    
                    const filterSidebarBtn = document.getElementById('filterSidebarBtn');
                    if (filterSidebarBtn) filterSidebarBtn.style.display = 'none';
                    
                    // Prevent direct access to filters page
                    if (currentPath === '/filters/') {
                        window.location.href = '/';
                        return;
                    }
                }
            } catch(e) {
                console.error("Error parsing user data:", e);
            }
        }

        // user is logged in
        if (authLinks) {
            let avatarUrl = "/media/avatars/default.jpg";
            if (userDataRaw) {
                try {
                    const user = JSON.parse(userDataRaw);
                    if (user.avatar) {
                        avatarUrl = user.avatar;
                    }
                } catch(e) {}
            }

            let extraIcon = '';
            if (currentPath === '/profile/') {
                extraIcon = `
                    <a href="#" style="display:flex; align-items:center; justify-content:center; width: 42px; height: 42px; border-radius: 50%; overflow:hidden; border: 2px solid var(--border-color, #e2e8f0); background: transparent; color: var(--text-primary, #334155); font-size: 20px; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" title="Sozlamalar">
                        <i class="fa-solid fa-gear"></i>
                    </a>
                `;
            }

            authLinks.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    ${extraIcon}
                    <a href="/profile/" class="nav-profile-pic" style="display:flex; align-items:center; justify-content:center; width: 42px; height: 42px; border-radius: 50%; overflow:hidden; border: 2px solid var(--accent-primary); transition: transform 0.3s ease; box-shadow: 0 4px 10px rgba(239, 108, 0, 0.2);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        <img src="${avatarUrl}" alt="Profile" style="width:100%; height:100%; object-fit:cover;" onerror="this.src='/media/avatars/default.jpg'">
                    </a>
                </div>
            `;
        }
    } else {
        // Redirect to login if user is not logged in and not already on auth pages
        if (currentPath !== '/login/' && currentPath !== '/register/') {
            window.location.href = '/login/';
            return;
        }

        // User is not logged in
        if (authLinks) {
            authLinks.innerHTML = `
                <a href="/login/" class="login-link">Kirish</a>
                <a href="/register/" class="login-link" style="margin-left: 10px;">Ro'yxatdan o'tish</a>
            `;
        }
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

    if (response.status === 401 || response.status === 403) {
        // Token might be expired. A real app would try to refresh here.
        // For now, just logout if unauthorized.
        logout();
    }

    return response;
}


