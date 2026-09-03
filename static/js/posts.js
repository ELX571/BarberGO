document.addEventListener('DOMContentLoaded', () => {
    fetchLatestPosts();
    fetchRecommendedPosts();

    // Set up search functionality
    const searchBtn = document.querySelector('.search-btn');
    const searchInput = document.querySelector('.search-input');
    
    // Custom Dropdown Logic
    const dropdown = document.getElementById('postFilterDropdown');
    const selectedBtn = document.getElementById('dropdownSelectedBtn');
    const selectedText = document.getElementById('dropdownSelectedText');
    const options = document.querySelectorAll('.dropdown-option');
    const recSection = document.getElementById('recommendedSection');
    const latestSection = document.getElementById('latestSection');

    if (dropdown && selectedBtn) {
        selectedBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('open');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            dropdown.classList.remove('open');
        });

        options.forEach(option => {
            option.addEventListener('click', () => {
                const value = option.getAttribute('data-value');
                const text = option.textContent;

                // Update UI
                selectedText.textContent = text;
                dropdown.setAttribute('data-value', value);
                options.forEach(opt => opt.classList.remove('active'));
                option.classList.add('active');
                dropdown.classList.remove('open');

                // Toggle sections
                if (value === 'latest') {
                    if (latestSection) latestSection.style.display = 'block';
                    if (recSection) recSection.style.display = 'none';
                } else if (value === 'location') {
                    if (latestSection) latestSection.style.display = 'none';
                    if (recSection) recSection.style.display = 'block';
                }

                // Refresh AOS
                setTimeout(() => {
                    if (typeof AOS !== 'undefined') AOS.refresh();
                }, 50);
            });
        });
    }

        if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => {
            const query = searchInput.value.trim();
            fetchLatestPosts(query);
            
            if (query) {
                // If searching, hide dropdown and recommended
                const filterContainer = document.querySelector('.post-filter-container');
                if (filterContainer) filterContainer.style.display = 'none';
                if (recSection) recSection.style.display = 'none';
                if (latestSection) latestSection.style.display = 'block';
            } else {
                // Restore filter state
                const filterContainer = document.querySelector('.post-filter-container');
                if (filterContainer) filterContainer.style.display = 'flex';
                // Trigger logic based on current dropdown value
                if (dropdown) {
                    const val = dropdown.getAttribute('data-value') || 'latest';
                    if (val === 'latest') {
                        if (latestSection) latestSection.style.display = 'block';
                        if (recSection) recSection.style.display = 'none';
                    } else {
                        if (latestSection) latestSection.style.display = 'none';
                        if (recSection) recSection.style.display = 'block';
                    }
                    setTimeout(() => {
                        if (typeof AOS !== 'undefined') AOS.refresh();
                    }, 50);
                }
            }
        });

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchBtn.click();
            }
        });
    }
});

function resolveMediaUrl(url) {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('//')) return url;
    if (url.startsWith('/')) return url;
    return `/${url}`;
}

function createPostCard(post) {
    let currentUserId = null;
    try {
        const uData = JSON.parse(localStorage.getItem('user_data'));
        if (uData && uData.id) currentUserId = uData.id;
    } catch(e) {}
    
    const userObj = post.user || {};
    const title = post.title || post.name || 'Barber Post';
    const excerpt = post.description || post.text || post.content || 'Check out this awesome barber style.';
    const imageUrl = resolveMediaUrl(post.image || post.photo) || 'https://images.unsplash.com/photo-1585747860715-2ba37e788b70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80';
    
    let authorName = userObj.first_name;
    if (userObj.last_name) authorName += ' ' + userObj.last_name;
    if (!authorName || authorName.trim() === '') authorName = userObj.username || 'Expert Barber';
    
    const avatarUrl = userObj.avatar || '/media/avatars/default.jpg';
    const date = post.created_at ? new Date(post.created_at).toLocaleDateString() : 'Recently';

    const likesCount = post.likes_count || 0;
    const isLiked = post.is_liked || false;
    const commentsCount = post.comments_count || 0;
    const bookmarksCount = post.bookmarks_count || 0;
    const isBookmarked = post.is_bookmarked || false;

    return `
        <div class="post-card glass-panel fade-in" data-aos="fade-up" data-aos-duration="600" data-aos-delay="100">
            <img src="${imageUrl}" alt="${title}" class="post-image" onerror="this.src='https://images.unsplash.com/photo-1585747860715-2ba37e788b70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'">
            <div class="post-content">
                <h3 class="post-title">${title}</h3>
                <p class="post-excerpt">${excerpt}</p>
                <div class="post-meta" style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                    <a href="/profile/${userObj.id}/" style="display:flex; align-items:center; gap:8px; text-decoration:none; color:inherit;">
                        <img src="${avatarUrl}" alt="avatar" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(authorName)}&background=random'">
                        <span class="author" style="font-weight:600;">${authorName}</span>
                    </a>
                    <span class="date" style="color:var(--text-muted); font-size:12px;">${date}</span>
                </div>
                
                <div class="post-actions" style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f3f4f6; padding-top:12px; margin-top:12px;">
                    <div style="display:flex; gap:16px;">
                        <button class="post-action-btn post-like-btn-${post.id}" onclick="togglePostLikeGlobal(${post.id})" style="background:none; border:none; cursor:pointer; font-size:15px; color:${isLiked ? '#ef4444' : '#6b7280'}; display:flex; align-items:center; gap:6px; transition:0.2s;">
                            <i class="fa-${isLiked ? 'solid' : 'regular'} fa-heart"></i>
                            <span class="like-count">${likesCount}</span>
                        </button>
                        <button class="post-action-btn post-comment-btn-${post.id}" onclick="openCommentsModalGlobal(${post.id})" style="background:none; border:none; cursor:pointer; font-size:15px; color:#6b7280; display:flex; align-items:center; gap:6px; transition:0.2s;">
                            <i class="fa-regular fa-comment"></i>
                            <span class="comment-count">${commentsCount}</span>
                        </button>
                    </div>
                    <button class="post-action-btn post-bookmark-btn-${post.id}" onclick="togglePostBookmarkGlobal(${post.id})" style="background:none; border:none; cursor:pointer; font-size:15px; color:${isBookmarked ? '#3b82f6' : '#6b7280'}; display:flex; align-items:center; gap:6px; transition:0.2s;">
                        <i class="fa-${isBookmarked ? 'solid' : 'regular'} fa-bookmark"></i>
                    </button>
                </div>
                ${(currentUserId !== userObj.id) ? `
                <button class="btn btn-primary" style="width:100%; margin-top:16px; border-radius:12px; font-weight:600; display:flex; justify-content:center; align-items:center; gap:8px; box-shadow:0 4px 12px rgba(249,115,22,0.25);" onclick="openContactModal(${userObj.id}, '${authorName}', '${userObj.phone_number || ''}', '${avatarUrl}')">
                    <i class="fa-solid fa-${userObj.role === 'customer' ? 'phone' : 'calendar-check'}" style="font-size:14px;"></i> ${userObj.role === 'customer' ? "Mijoz bilan bog'lanish" : "Bron qilish"}
                </button>
                ` : ''}
            </div>
        </div>
    `;
}

async function fetchLatestPosts(searchQuery = '') {
    const grid = document.getElementById('latestPostsGrid');
    const section = document.getElementById('latestSection');
    const title = section ? section.querySelector('.section-title') : null;
    
    try {
        let url = '/posts/posts/';

        const response = await apiCall(url);
        const data = await response.json();
        console.log("API dan kelgan postlar:", data);
        
        if (!response.ok) {
            throw new Error(data.detail || data.error || 'Server xatosi');
        }
        
        let posts = Array.isArray(data) ? data : (data.results || []);

        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            posts = posts.filter(post => {
                const titleMatch = (post.title || post.name || '').toLowerCase().includes(query);
                const descMatch = (post.description || post.text || post.content || '').toLowerCase().includes(query);
                const authorMatch = (post.author?.first_name || post.barber?.first_name || '').toLowerCase().includes(query);
                return titleMatch || descMatch || authorMatch;
            });
            
            if (title) title.textContent = 'Qidiruv Natijalari';
        } else {
            if (title) title.textContent = 'So\'nggi Postlar';
        }

        const dropdown = document.getElementById('postFilterDropdown');
        const isActiveTab = (!dropdown || dropdown.getAttribute('data-value') === 'latest' || !dropdown.getAttribute('data-value')) && !searchQuery;

        if (posts.length === 0) {
            grid.innerHTML = '<p style="padding: 20px; color: var(--text-secondary); grid-column: 1/-1; text-align: center;">Hech narsa topilmadi...</p>';
            if(section && (isActiveTab || searchQuery)) section.style.display = 'block';
            return;
        }

        if(section && (isActiveTab || searchQuery)) section.style.display = 'block';
        grid.innerHTML = posts.map(createPostCard).join('');
        
        setTimeout(() => {
            if (typeof AOS !== 'undefined') AOS.refresh();
        }, 100);
        
    } catch (error) {
        console.error('Error fetching posts:', error);
        grid.innerHTML = '<p style="padding: 20px; color: var(--error); grid-column: 1/-1; text-align: center;">Xatolik yuz berdi. Qaytadan urinib ko\'ring.</p>';
        const dropdown = document.getElementById('postFilterDropdown');
        if(section && (!dropdown || dropdown.getAttribute('data-value') === 'latest' || !dropdown.getAttribute('data-value'))) section.style.display = 'block';
    }
}

async function fetchRecommendedPosts() {
    const token = localStorage.getItem('access_token');
    const section = document.getElementById('recommendedSection');
    const grid = document.getElementById('recommendedPostsGrid');
    
    if (!token) {
        if (grid) grid.innerHTML = '<p style="padding: 20px; color: var(--text-secondary); grid-column: 1/-1; text-align: center;">Tavsiyalarni ko\'rish uchun tizimga kiring.</p>';
        return;
    }

    try {
        const response = await apiCall('/posts/recommended-posts/');
        if (!response.ok) {
            if (grid) grid.innerHTML = '<p style="padding: 20px; color: var(--text-secondary); grid-column: 1/-1; text-align: center;">Tavsiyalar hozircha mavjud emas.</p>';
            return;
        }

        const data = await response.json();
        const posts = Array.isArray(data) ? data : (data.results || []);

        if (posts.length > 0) {
            const dropdown = document.getElementById('postFilterDropdown');
            if (dropdown && dropdown.getAttribute('data-value') === 'location') {
                section.style.display = 'block';
            }
            grid.innerHTML = posts.map(createPostCard).join('');
            
            // Refresh AOS
            setTimeout(() => {
                if (typeof AOS !== 'undefined') AOS.refresh();
            }, 100);
        } else {
            if (grid) grid.innerHTML = '<p style="padding: 20px; color: var(--text-secondary); grid-column: 1/-1; text-align: center;">Sizning hududingizda postlar topilmadi.</p>';
        }
        
    } catch (error) {
        console.error('Error fetching recommended posts:', error);
        if (grid) grid.innerHTML = '<p style="padding: 20px; color: var(--text-secondary); grid-column: 1/-1; text-align: center;">Xatolik yuz berdi.</p>';
    }
}
