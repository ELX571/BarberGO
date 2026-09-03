import re

# Update notifications/views.py
with open("notifications/views.py", "r") as f:
    notif_views = f.read()

notif_views = notif_views.replace(
    "def notify_user(user_id, message):",
    "def notify_user(user_id, message, order_id=None):"
)
notif_views = notif_views.replace(
    "'message': message",
    "'message': message,\n            'order_id': order_id"
)

# Also update the API to return order_id
notif_views = notif_views.replace(
    "'message': n.description,",
    "'message': n.description,\n            'order_id': n.order_id,"
)

with open("notifications/views.py", "w") as f:
    f.write(notif_views)

# Update notifications/consumer.py
with open("notifications/consumer.py", "r") as f:
    consumer_py = f.read()
consumer_py = consumer_py.replace(
    "'message': event['message']",
    "'message': event['message'],\n            'order_id': event.get('order_id')"
)
with open("notifications/consumer.py", "w") as f:
    f.write(consumer_py)

# Update orders/views.py
with open("orders/views.py", "r") as f:
    orders_views = f.read()

orders_views = orders_views.replace(
    "Notifications.objects.create(",
    "Notifications.objects.create(\n            order_id=order.id,"
)
orders_views = orders_views.replace(
    "notify_user(order.barber.id, message)",
    "notify_user(order.barber.id, message, order_id=order.id)"
)
with open("orders/views.py", "w") as f:
    f.write(orders_views)
