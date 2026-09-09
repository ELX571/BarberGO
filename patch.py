with open("/app/orders/views.py", "r") as f:
    text = f.read()

text = text.replace(
    "order.status = status\n        order.save()",
    "order.status = status\n        order.save()\n        \n        from notifications.models import Notifications\n        if status == Order.Status.ACCEPTED:\n            Notifications.objects.filter(order_id=order.id, receptions=request.user).update(description='Ushbu bron qabul qilindi.')\n        elif status == Order.Status.CANCELED:\n            Notifications.objects.filter(order_id=order.id, receptions=request.user).update(description='Ushbu bron bekor qilindi.')"
)

with open("/app/orders/views.py", "w") as f:
    f.write(text)
