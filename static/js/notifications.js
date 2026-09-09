// ─── NOTIFICATIONS MODULE ───────────────────────
const NOTIF_STORAGE_KEY = 'barbergo_notifications';
let notifSocket = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        hide('notifList');
        hide('notifEmpty');
        show('notifAuth');
        updateWsStatus('error', 'Tizimga kirilmagan');
        return;
    }

    renderNotifications();
    connectWebSocket();
});

// ─── WEBSOCKET ──────────────────────────────────
function connectWebSocket() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    const wsProtocol = location.protocol === 'https:' ? 'wss' : 'ws';
    const wsUrl = `${wsProtocol}://${location.host}/ws/notifications/?token=${token}`;

    updateWsStatus('connecting', 'Ulanmoqda...');

    try {
        notifSocket = new WebSocket(wsUrl);

        notifSocket.onopen = () => {
            updateWsStatus('connected', 'Ulangan (real-time)');
        };

        notifSocket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const notification = {
                    id: Date.now(),
                    title: 'Yangi bildirishnoma',
                    message: data.message || data.text || 'Yangi xabar keldi',
                    order_id: data.order_id || null,
                    time: new Date().toISOString(),
                    read: false
                };
                addNotification(notification);
                renderNotifications();
                updateSidebarBadge();
            } catch (e) {
                console.error('Notification parse error:', e);
            }
        };

        notifSocket.onclose = () => {
            updateWsStatus('error', 'Uzildi. 5 soniyada qayta ulanadi...');
            setTimeout(connectWebSocket, 5000);
        };

        notifSocket.onerror = () => {
            updateWsStatus('error', 'Ulanishda xatolik');
        };

    } catch (e) {
        updateWsStatus('error', 'WebSocket qo\'llab-quvvatlanmaydi');
    }
}

function updateWsStatus(state, text) {
    const dot = document.getElementById('wsDot');
    const label = document.getElementById('wsText');
    if (!dot || !label) return;

    dot.className = 'ws-dot';
    if (state === 'connected') dot.classList.add('connected');
    else if (state === 'error') dot.classList.add('error');
    label.textContent = text;
}

// ─── LOCAL STORAGE ──────────────────────────────
function getNotifications() {
    try {
        return JSON.parse(localStorage.getItem(NOTIF_STORAGE_KEY)) || [];
    } catch (e) {
        return [];
    }
}

function saveNotifications(notifs) {
    localStorage.setItem(NOTIF_STORAGE_KEY, JSON.stringify(notifs));
}

function addNotification(notif) {
    const notifs = getNotifications();
    notifs.unshift(notif);
    // Keep max 100
    if (notifs.length > 100) notifs.length = 100;
    saveNotifications(notifs);
}

// ─── RENDER ─────────────────────────────────────
function renderNotifications() {
    const list = document.getElementById('notifList');
    const emptyState = document.getElementById('notifEmpty');
    if (!list || !emptyState) return;

    const notifs = getNotifications();

    if (notifs.length === 0) {
        list.innerHTML = '';
        show('notifEmpty');
        return;
    }

    hide('notifEmpty');

    list.innerHTML = notifs.map((n, i) => {
        const timeAgo = getTimeAgo(n.time);
        const unreadClass = n.read ? '' : 'unread';

        return `
            <div class="notif-card ${unreadClass}" data-index="${i}" onclick="markAsRead(${i})">
                <div class="notif-icon">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                    </svg>
                </div>
                <div class="notif-body">
                    <div class="notif-title">${escapeHtml(n.title || 'Bildirishnoma')}</div>
                    <div class="notif-message">${escapeHtml(n.message)}</div>
                    <div class="notif-time">${timeAgo}</div>
                </div>

                <div class="notif-actions-inline">
                    ${n.order_id && !n.message.includes('qabul qildi') && !n.message.includes('bekor qildi') ? `
                        <button class="action-btn accept-btn" onclick="event.stopPropagation(); changeOrderStatus(${n.order_id}, 'accept')" style="background: rgba(34,197,94,0.1); color: #22c55e; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 4px; font-size:12px;">Qabul qilish</button>
                        <button class="action-btn cancel-btn" onclick="event.stopPropagation(); changeOrderStatus(${n.order_id}, 'cancel')" style="background: rgba(239,68,68,0.1); color: #ef4444; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 8px; font-size:12px;">Bekor qilish</button>
                    ` : ''}
                    <button class="notif-dismiss" onclick="event.stopPropagation(); removeNotification(${i})" title="O'chirish">

                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                </div>
            </div>
        `;
    }).join('');

    updateSidebarBadge();
}

// ─── ACTIONS ────────────────────────────────────
function markAsRead(index) {
    const notifs = getNotifications();
    if (notifs[index]) {
        notifs[index].read = true;
        saveNotifications(notifs);
        renderNotifications();
    }
}

function markAllRead() {
    const notifs = getNotifications();
    notifs.forEach(n => n.read = true);
    saveNotifications(notifs);
    renderNotifications();
}

function removeNotification(index) {
    const notifs = getNotifications();
    notifs.splice(index, 1);
    saveNotifications(notifs);
    renderNotifications();
}

function clearAllNotifications() {
    if (!confirm("Barcha bildirishnomalarni o'chirmoqchimisiz?")) return;
    saveNotifications([]);
    renderNotifications();
}

// ─── SIDEBAR BADGE ──────────────────────────────
function updateSidebarBadge() {
    const notifs = getNotifications();
    const unreadCount = notifs.filter(n => !n.read).length;
    
    // Find notifications sidebar link
    const notifLink = document.querySelector('a[href="/notifications/"]');
    if (!notifLink) return;

    // Remove existing badge
    const existing = notifLink.querySelector('.notif-badge');
    if (existing) existing.remove();

    // Add badge if unread > 0
    if (unreadCount > 0) {
        notifLink.style.position = 'relative';
        const badge = document.createElement('span');
        badge.className = 'notif-badge';
        badge.textContent = unreadCount > 9 ? '9+' : unreadCount;
        notifLink.appendChild(badge);
    }
}

// ─── HELPERS ────────────────────────────────────
function getTimeAgo(dateStr) {
    const now = new Date();
    const date = new Date(dateStr);
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return 'Hozirgina';
    if (diff < 3600) return `${Math.floor(diff / 60)} daqiqa oldin`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} soat oldin`;
    if (diff < 604800) return `${Math.floor(diff / 86400)} kun oldin`;
    return date.toLocaleDateString('uz-UZ');
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

function show(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'block';
}

function hide(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
}


// ─── ACCEPT / CANCEL ORDER FROM NOTIFICATION ───
window.changeOrderStatus = window.changeOrderStatus || async function(orderId, action) {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
        const response = await fetch(`/orders/${orderId}/${action}/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert('Buyurtma holati o\'zgartirildi!');
            window.location.reload();
        } else {
            const data = await response.json();
            alert(data.detail || data.error || 'Xatolik yuz berdi');
        }
    } catch (e) {
        alert('Tarmoq xatosi.');
    }
}
