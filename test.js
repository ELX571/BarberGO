    <script>
        const API = {
            posts: '/posts/posts/',
            login: '/accounts/auth-jwt/login/',
            me: '/accounts/auth-jwt/me/',
            register: '/step-2/',
        };

        function getToken() {
            const raw = localStorage.getItem('access_token');
            if (!raw) return '';
            return String(raw).trim().replace(/^Bearer\s+/i, '').replace(/^"|"$/g, '');
        }

        function decodeJwtPayload(token) {
            try {
                const payload = token.split('.')[1];
                const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(payload.length / 4) * 4, '='));
                return JSON.parse(json);
            } catch {
                return null;
            }
        }

        function escapeHtml(value) {
            return String(value ?? '')
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        function formatUserLabel(user) {
            if (user && typeof user === 'object') {
                return user.username ? `@${user.username}` : (user.id ? `User #${user.id}` : '-');
            }
            return user ? `User #${user}` : '-';
        }

        function csrfToken() {
            const el = document.querySelector('[name=csrfmiddlewaretoken]');
            return el ? el.value : '';
        }

        function showToast(type, message) {
            const toastEl = document.getElementById('toastNotif');
            const iconEl = document.getElementById('toastIcon');
            const msgEl = document.getElementById('toastMsg');
            const configs = {
                success: { icon: '<i class="fa-solid fa-check"></i>', bg: 'linear-gradient(135deg, #10b981, #059669)' },
                error: { icon: '<i class="fa-solid fa-xmark"></i>', bg: 'linear-gradient(135deg, #ef4444, #dc2626)' },
                warning: { icon: '<i class="fa-solid fa-exclamation"></i>', bg: 'linear-gradient(135deg, #f59e0b, #d97706)' },
                info: { icon: '<i class="fa-solid fa-info"></i>', bg: 'linear-gradient(135deg, #3b82f6, #2563eb)' }
            };
            const cfg = configs[type] || configs.info;
            iconEl.innerHTML = cfg.icon;
            iconEl.style.background = cfg.bg;
            msgEl.textContent = message;
            toastEl.style.display = 'flex';
            clearTimeout(toastEl._timeout);
            toastEl._timeout = setTimeout(() => { toastEl.style.display = 'none'; }, 2800);
        }

        function authHeaders(extra = {}) {
            const token = getToken();
            const headers = { ...extra };
            if (token) headers.Authorization = 'Bearer ' + token;
            return headers;
        }

        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            document.getElementById('themeIcon').className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        }

        function initTheme() {
            const saved = localStorage.getItem('theme') || 'light';
            setTheme(saved);
            document.getElementById('themeBtn').addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme');
                setTheme(current === 'dark' ? 'light' : 'dark');
            });
        }

        function renderHeader() {
            const headerRight = document.getElementById('headerRight');
            const token = getToken();
            const payload = token ? (decodeJwtPayload(token) || {}) : {};
            const username = payload.username || 'user';
            
            headerRight.innerHTML = `
                <span style="font-size:13px;color:var(--text-muted);font-weight:700;">@${username}</span>
                <img src="https://ui-avatars.com/api/?name=${username}&background=random" class="profile-avatar" alt="Profile">
                <button type="button" class="btn-link" id="logoutBtn" style="padding: 10px 14px;"><i class="fa-solid fa-arrow-right-from-bracket"></i></button>
            `;

            const logoutBtn = document.getElementById('logoutBtn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', () => {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.reload();
                });
            }
        }

        async function fetchPosts() {
            const res = await fetch(API.posts, { headers: authHeaders() });
            if (!res.ok) {
                const msg = res.status === 401 || res.status === 403
                    ? 'Postlarni ko‘rish uchun tizimga kiring'
                    : 'Postlar yuklanmadi';
                showToast('warning', msg);
                return [];
            }
            return await res.json();
        }

        function postHtml(post, currentUserId) {
            const title = escapeHtml(post.title || 'Post');
            const description = escapeHtml(post.description || '').replace(/\n/g, '<br>');
            const image = post.image ? `<img src="${escapeHtml(post.image)}" class="post-image" alt="post image">` : '';
            const video = post.video ? `<a href="${escapeHtml(post.video)}" target="_blank" rel="noopener noreferrer" class="btn-link" style="width:max-content;">{% trans "Video" %}</a>` : '';
            const canEdit = currentUserId && String(currentUserId) === String(post.user);
            const likes = Number(post.like_count ?? post.likes ?? 0);
            return `
                <article class="post-card" data-search="${escapeHtml((post.title || '') + ' ' + (post.description || '')).toLowerCase()}">
                    <div class="post-top">
                        <div class="post-meta">
                            <div class="post-title">${title}</div>
                            <div class="post-sub">${formatUserLabel(post.user)} · ${escapeHtml(post.created_at || '')}</div>
                        </div>
                        <div class="post-sub">${post.id ? '#' + post.id : ''}</div>
                    </div>
                    <div class="post-body">${description}</div>
                    ${image}
                    <div style="display:flex;gap:10px;flex-wrap:wrap;">${video}</div>
                    <div class="post-actions">
                        <div class="action-group">
                            <button type="button" class="action-btn like" data-id="${post.id}">
                                <i class="fa-regular fa-heart"></i> <span class="like-count">${likes}</span>
                            </button>
                        </div>
                        ${canEdit ? `
                            <div class="action-group">
                                <button type="button" class="action-btn" data-edit="${post.id}"><i class="fa-regular fa-pen-to-square"></i> {% trans "Tahrirlash" %}</button>
                                <button type="button" class="action-btn danger" data-delete="${post.id}"><i class="fa-regular fa-trash-can"></i> {% trans "O'chirish" %}</button>
                            </div>
                        ` : ''}
                    </div>
                </article>
            `;
        }

        async function renderFeed() {
            const token = getToken();
            const postsContainer = document.getElementById('postsContainer');
            postsContainer.innerHTML = `<div class="empty-state">{% trans "Yuklanmoqda..." %}</div>`;

            if (!token) {
                document.getElementById('composeBox').style.display = 'none';
                postsContainer.innerHTML = `<div class="empty-state">{% trans "Postlarni ko'rish va yaratish uchun avval ro'yxatdan o'ting." %}</div>`;
                return;
            }

            document.getElementById('openComposeBtn').style.display = 'inline-flex';
            const payload = decodeJwtPayload(token) || {};
            const currentUserId = payload.user_id;
            const posts = await fetchPosts();
            if (!posts || !posts.length) {
                postsContainer.innerHTML = `<div class="empty-state">{% trans "Hozircha postlar yo'q." %}</div>`;
                return;
            }
            
            posts.reverse();

            postsContainer.innerHTML = posts.map(p => postHtml(p, currentUserId)).join('');
            bindPostActions();
            applySearchFilter();
        }

        function bindPostActions() {
            document.querySelectorAll('[data-id]').forEach(btn => {
                btn.addEventListener('click', () => toggleLike(btn.dataset.id, btn));
            });
            document.querySelectorAll('[data-edit]').forEach(btn => {
                btn.addEventListener('click', () => openEditModal(btn.dataset.edit));
            });
            document.querySelectorAll('[data-delete]').forEach(btn => {
                btn.addEventListener('click', () => removePost(btn.dataset.delete));
            });
        }

        async function toggleLike(postId, btn) {
            const res = await fetch(`${API.posts}${postId}/like/`, {
                method: 'POST',
                headers: authHeaders({ 'X-CSRFToken': csrfToken() })
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) {
                showToast('error', data.detail || data.error || '{% trans "Like xatosi" %}');
                return;
            }
            const icon = btn.querySelector('i');
            const count = btn.querySelector('.like-count');
            if (data.like) {
                btn.classList.add('liked');
                icon.className = 'fa-solid fa-heart';
            } else {
                btn.classList.remove('liked');
                icon.className = 'fa-regular fa-heart';
            }
            if (count) count.textContent = data.likes ?? '';
        }

        async function removePost(postId) {
            if (!confirm('{% trans "Postni o\'chirishni tasdiqlaysizmi?" %}')) return;
            const res = await fetch(`${API.posts}${postId}/`, {
                method: 'DELETE',
                headers: authHeaders({ 'X-CSRFToken': csrfToken() })
            });
            if (res.ok) {
                showToast('success', '{% trans "Post o\'chirildi" %}');
                renderFeed();
            } else {
                showToast('error', '{% trans "O\'chirish amalga oshmadi" %}');
            }
        }

        let editingPostId = null;
        function openEditModal(postId) {
            editingPostId = postId;
            const card = [...document.querySelectorAll('.post-card')].find(el => el.querySelector('[data-edit="'+postId+'"]'));
            const title = card?.querySelector('.post-title')?.textContent || '';
            const body = card?.querySelector('.post-body')?.textContent || '';
            document.getElementById('editPostId').value = postId;
            document.getElementById('editPostTitle').value = title;
            document.getElementById('editPostDescription').value = body;
            document.getElementById('editModal').style.display = 'flex';
        }

        function closeEditModal() {
            document.getElementById('editModal').style.display = 'none';
            editingPostId = null;
        }

        async function createPost(formData) {
            const res = await fetch(API.posts, {
                method: 'POST',
                headers: authHeaders({ 'X-CSRFToken': csrfToken() }),
                body: formData
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.detail || data.error || '{% trans "Post yaratilmadi" %}');
        }

        async function updatePost(postId, formData) {
            const res = await fetch(`${API.posts}${postId}/`, {
                method: 'PUT',
                headers: authHeaders({ 'X-CSRFToken': csrfToken() }),
                body: formData
            });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.detail || data.error || '{% trans "Post yangilanmadi" %}');
        }

        document.getElementById('composeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData();
            fd.append('title', document.getElementById('postTitle').value.trim());
            fd.append('description', document.getElementById('postDescription').value.trim());
            const img = document.getElementById('postImage').files[0];
            const vid = document.getElementById('postVideo').files[0];
            if (img) fd.append('image', img);
            if (vid) fd.append('video', vid);
            try {
                await createPost(fd);
                showToast('success', '{% trans "Post yaratildi" %}');
                e.target.reset();
                document.getElementById('composeBox').style.display = 'none';
                renderFeed();
            } catch (err) {
                showToast('error', err.message);
            }
        });

        document.getElementById('editForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData();
            fd.append('title', document.getElementById('editPostTitle').value.trim());
            fd.append('description', document.getElementById('editPostDescription').value.trim());
            const img = document.getElementById('editPostImage').files[0];
            const vid = document.getElementById('editPostVideo').files[0];
            if (img) fd.append('image', img);
            if (vid) fd.append('video', vid);
            try {
                await updatePost(editingPostId, fd);
                showToast('success', '{% trans "Post yangilandi" %}');
                closeEditModal();
                renderFeed();
            } catch (err) {
                showToast('error', err.message);
            }
        });

        function applySearchFilter() {
            const input = document.getElementById('searchInput');
            const filter = () => {
                const q = input.value.trim().toLowerCase();
                document.querySelectorAll('.post-card').forEach(card => {
                    const text = card.getAttribute('data-search') || '';
                    card.style.display = text.includes(q) ? '' : 'none';
                });
            };
            input.oninput = filter;
            filter();
        }

        document.getElementById('refreshBtn').addEventListener('click', renderFeed);
        document.getElementById('openComposeBtn').addEventListener('click', () => {
            document.getElementById('composeBox').style.display = 'block';
            document.getElementById('composeBox').scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        document.getElementById('closeComposeBtn').addEventListener('click', () => {
            document.getElementById('composeBox').style.display = 'none';
        });
        document.getElementById('closeEditBtn').addEventListener('click', closeEditModal);
        document.getElementById('editModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) closeEditModal();
        });

        initTheme();
        renderHeader();
        renderFeed();
    </script>
