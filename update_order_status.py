with open("orders/views.py", "r") as f:
    text = f.read()

text = text.replace(
    "order.status = status\n        order.save()",
    "order.status = status\n        order.save()\n        \n        # Update notification text so buttons disappear\n        from notifications.models import Notifications\n        if status == Order.Status.ACCEPTED:\n            Notifications.objects.filter(order_id=order.id, receptions=request.user).update(description=order.customer.get_full_name() + ' tomonidan qilingan bron qabul qilindi.')\n        elif status == Order.Status.CANCELED:\n            Notifications.objects.filter(order_id=order.id, receptions=request.user).update(description=order.customer.get_full_name() + ' tomonidan qilingan bron bekor qilindi.')"
)

with open("orders/views.py", "w") as f:
    f.write(text)
