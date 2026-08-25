let allOrders = [];
let currentFilter = 'all';
let userRole = null;

document.addEventListener('DOMContentLoaded', () => {
    // Determine user role
    const userDataRaw = localStorage.getItem('user_data');
    if (userDataRaw) {
        try {
            const user = JSON.parse(userDataRaw);
            userRole = user.role;
        } catch(e) {}
    }

    // Show "Yangi Buyurtma" button only for customers
    const createBtn = document.getElementById('createOrderBtn');
    if (userRole === 'customer' && createBtn) {
        createBtn.style.display = 'inline-flex';
    }

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderOrders();
        });
    });

    // Create order form
    const form = document.getElementById('createOrderForm');
    if (form) {
        form.addEventListener('submit', handleCreateOrder);
    }

    fetchOrders();
});

// ─── FETCH ORDERS ───────────────────────────────
async function fetchOrders() {
    const token = localStorage.getItem('access_token');
    const loadingState = document.getElementById('ordersLoading');
    const authState = document.getElementById('authRequired');

    if (!token) {
        loadingState.style.display = 'none';
        authState.style.display = 'block';
        return;
    }

    try {
        const response = await apiCall('/orders/');
        if (!response.ok) throw new Error('Failed to fetch');

        const data = await response.json();
        allOrders = Array.isArray(data) ? data : (data.results || []);

        loadingState.style.display = 'none';
        renderOrders();

    } catch (err) {
        console.error('Error fetching orders:', err);
        loadingState.style.display = 'none';
        document.getElementById('ordersEmpty').innerHTML = '<p style="color:#ef4444;">Buyurtmalarni yuklashda xatolik.</p>';
        document.getElementById('ordersEmpty').style.display = 'block';
    }
}

// ─── RENDER ORDERS ──────────────────────────────
function renderOrders() {
    const list = document.getElementById('ordersList');
    const emptyState = document.getElementById('ordersEmpty');

    const filtered = currentFilter === 'all'
        ? allOrders
        : allOrders.filter(o => o.status === currentFilter);

    if (filtered.length === 0) {
        list.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    list.innerHTML = filtered.map(order => {
        const statusLabels = {
            'pending': 'Kutilmoqda',
            'accepted': 'Qabul qilingan',
            'canceled': 'Bekor qilingan'
        };

        const statusClass = `status-${order.status || 'pending'}`;
        const statusLabel = statusLabels[order.status] || order.status;

        const desc = order.description || 'Tavsif yo\'q';
        const time = order.endpoint_time
            ? new Date(order.endpoint_time).toLocaleString('uz-UZ', { day:'numeric', month:'long', year:'numeric', hour:'2-digit', minute:'2-digit' })
            : '—';
        const created = order.created_at
            ? new Date(order.created_at).toLocaleDateString('uz-UZ')
            : '';

        // Who is the other party
        let partyLabel = '';
        if (userRole === 'customer') {
            partyLabel = `Sartarosh: #${order.barber}`;
        } else if (userRole === 'barber') {
            partyLabel = `Mijoz: #${order.customer}`;
        }

        // Action buttons: only barber can accept/cancel pending orders
        let actionsHtml = `<span class="status-badge ${statusClass}">${statusLabel}</span>`;
        if (userRole === 'barber' && order.status === 'pending') {
            actionsHtml = `
                <button class="action-btn accept-btn" onclick="changeOrderStatus(${order.id}, 'accept')">
                    ✓ Qabul qilish
                </button>
                <button class="action-btn cancel-btn" onclick="changeOrderStatus(${order.id}, 'cancel')">
                    ✕ Bekor qilish
                </button>
            `;
        }
        actionsHtml += `<a href="/chat/${order.id}/" class="action-btn" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px;">💬 Chat</a>`;

        return `
            <div class="order-card" data-status="${order.status}">
                <div class="order-info">
                    <h3>${desc.length > 60 ? desc.substring(0, 60) + '...' : desc}</h3>
                    <p>${partyLabel}</p>
                    <div class="order-meta">
                        <span>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                            ${time}
                        </span>
                        <span>Yaratilgan: ${created}</span>
                    </div>
                </div>
                <div class="order-actions">
                    ${actionsHtml}
                </div>
            </div>
        `;
    }).join('');
}

// ─── CREATE ORDER (Customer only) ───────────────
async function handleCreateOrder(e) {
    e.preventDefault();
    const errorDiv = document.getElementById('orderError');
    errorDiv.style.display = 'none';

    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerText;
    btn.innerText = 'Yuborilmoqda...';
    btn.disabled = true;

    const token = localStorage.getItem('access_token');
    if (!token) {
        errorDiv.innerText = 'Avval tizimga kiring!';
        errorDiv.style.display = 'block';
        btn.innerText = originalText;
        btn.disabled = false;
        return;
    }

    const formData = new FormData();
    formData.append('barber', document.getElementById('orderBarber').value);
    formData.append('description', document.getElementById('orderDescription').value);
    formData.append('endpoint_time', document.getElementById('orderTime').value);

    const imageFile = document.getElementById('orderImage').files[0];
    if (imageFile) formData.append('image', imageFile);

    try {
        const response = await fetch('/orders/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok || response.status === 201) {
            closeOrderModal();
            document.getElementById('createOrderForm').reset();
            // Re-fetch orders
            document.getElementById('ordersLoading').style.display = 'block';
            fetchOrders();
        } else {
            let errorMsg = 'Xatolik yuz berdi!';
            if (data.error) errorMsg = data.error;
            else if (data.detail) errorMsg = data.detail;
            else if (typeof data === 'object') {
                const firstKey = Object.keys(data)[0];
                if (Array.isArray(data[firstKey])) {
                    errorMsg = `${firstKey}: ${data[firstKey][0]}`;
                } else {
                    errorMsg = `${firstKey}: ${data[firstKey]}`;
                }
            }
            errorDiv.innerText = errorMsg;
            errorDiv.style.display = 'block';
        }
    } catch (err) {
        errorDiv.innerText = 'Tarmoq xatosi. Qayta urinib ko\'ring.';
        errorDiv.style.display = 'block';
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

// ─── ACCEPT / CANCEL (Barber only) ──────────────
async function changeOrderStatus(orderId, action) {
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
            // Update local state immediately
            const order = allOrders.find(o => o.id === orderId);
            if (order) {
                order.status = action === 'accept' ? 'accepted' : 'canceled';
            }
            renderOrders();
        } else {
            const data = await response.json();
            alert(data.detail || data.error || 'Xatolik yuz berdi');
        }
    } catch (err) {
        alert('Tarmoq xatosi');
    }
}

// ─── MODAL ──────────────────────────────────────
function openOrderModal() {
    document.getElementById('orderModal').classList.add('open');
    document.getElementById('orderError').style.display = 'none';
}

function closeOrderModal() {
    document.getElementById('orderModal').classList.remove('open');
}

// Close modal on overlay click
document.getElementById('orderModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'orderModal') closeOrderModal();
});

