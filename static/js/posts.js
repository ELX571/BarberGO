document.addEventListener('DOMContentLoaded', () => {
    fetchLatestPosts();
    fetchRecommendedPosts();
});

function createPostCard(post) {
    // Assuming post has id, title, description/excerpt, image/photo, author etc based on standard DRF models.
    const title = post.title || post.name || 'Barber Post';
    const excerpt = post.description || post.text || post.content || 'Check out this awesome barber style.';
    const imageUrl = post.image || post.photo || 'https://images.unsplash.com/photo-1585747860715-2ba37e788b70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80';
    const author = post.author?.first_name || post.barber?.first_name || 'Expert Barber';
    const date = post.created_at ? new Date(post.created_at).toLocaleDateString() : 'Recently';

    return `
        <div class="post-card glass-panel fade-in">
            <img src="${imageUrl}" alt="${title}" class="post-image" onerror="this.src='https://images.unsplash.com/photo-1585747860715-2ba37e788b70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'">
            <div class="post-content">
                <h3 class="post-title">${title}</h3>
                <p class="post-excerpt">${excerpt}</p>
                <div class="post-meta">
                    <span>By ${author}</span>
                    <span>${date}</span>
                </div>
            </div>
        </div>
    `;
}

async function fetchLatestPosts() {
    const grid = document.getElementById('latestPostsGrid');
    
    try {
        const response = await apiCall('/posts/posts/');
        const data = await response.json();
        
        // Data might be paginated (e.g. data.results) or a flat array
        const posts = Array.isArray(data) ? data : (data.results || []);

        if (posts.length === 0) {
            grid.innerHTML = '<div class="empty-state">No posts available right now.</div>';
            return;
        }

        grid.innerHTML = posts.map(createPostCard).join('');
        
    } catch (error) {
        console.error('Error fetching posts:', error);
        grid.innerHTML = '<div class="empty-state" style="color: var(--danger);">Failed to load posts. Please try again later.</div>';
    }
}

async function fetchRecommendedPosts() {
    const token = localStorage.getItem('access_token');
    // If not logged in, maybe don't show recommended, or API might fail
    if (!token) return;

    const section = document.getElementById('recommendedSection');
    const grid = document.getElementById('recommendedPostsGrid');
    
    try {
        const response = await apiCall('/posts/recommended-posts/');
        if (!response.ok) return; // Silent fail if unauthorized or not found

        const data = await response.json();
        const posts = Array.isArray(data) ? data : (data.results || []);

        if (posts.length > 0) {
            section.style.display = 'block';
            grid.innerHTML = posts.map(createPostCard).join('');
        }
        
    } catch (error) {
        console.error('Error fetching recommended posts:', error);
    }
}
