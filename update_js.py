import re

# Update notifications.html
with open("Templates/notifications.html", "r") as f:
    html = f.read()

html = html.replace(
    "message: \"{{ notif.description|escapejs }}\",",
    "message: \"{{ notif.description|escapejs }}\",\n            order_id: {% if notif.order_id %}{{ notif.order_id }}{% else %}null{% endif %},"
)
with open("Templates/notifications.html", "w") as f:
    f.write(html)

# Update notifications.js
with open("static/js/notifications.js", "r") as f:
    js = f.read()

js = js.replace(
    "message: data.message || data.text || 'Yangi xabar keldi',",
    "message: data.message || data.text || 'Yangi xabar keldi',\n                    order_id: data.order_id || null,"
)

# Add accept/reject buttons to renderNotifications
new_render = """
                <div class="notif-actions-inline">
                    ${n.order_id && !n.message.includes('qabul qildi') && !n.message.includes('bekor qildi') ? `
                        <button class="action-btn accept-btn" onclick="event.stopPropagation(); changeOrderStatus(${n.order_id}, 'accept')" style="background: rgba(34,197,94,0.1); color: #22c55e; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 4px; font-size:12px;">Qabul qilish</button>
                        <button class="action-btn cancel-btn" onclick="event.stopPropagation(); changeOrderStatus(${n.order_id}, 'cancel')" style="background: rgba(239,68,68,0.1); color: #ef4444; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 8px; font-size:12px;">Bekor qilish</button>
                    ` : ''}
                    <button class="notif-dismiss" onclick="event.stopPropagation(); removeNotification(${i})" title="O'chirish">
"""
js = js.replace(
    """                <div class="notif-actions-inline">
                    <button class="notif-dismiss" onclick="event.stopPropagation(); removeNotification(${i})" title="O'chirish">""",
    new_render
)

# Also we need to make sure changeOrderStatus is available or redirect to orders
# Instead of duplicating changeOrderStatus, let's just make it redirect to /orders-ui/ or define it here if it's missing.
# Let's add a simple fetch inside notifications.js if changeOrderStatus doesn't exist.
redirect_logic = """
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
            alert('Buyurtma holati o\\'zgartirildi!');
            window.location.reload();
        } else {
            const data = await response.json();
            alert(data.detail || data.error || 'Xatolik yuz berdi');
        }
    } catch (e) {
        alert('Tarmoq xatosi.');
    }
}
"""
if "window.changeOrderStatus" not in js:
    js += "\n" + redirect_logic

with open("static/js/notifications.js", "w") as f:
    f.write(js)
