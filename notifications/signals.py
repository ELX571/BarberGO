from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.views import notify_user
from orders.models import Order


@receiver(post_save, sender=Order)
def order_notifications_save(sender, instance, created, **kwargs):
    if not created:
        return

    barber = instance.barber
    if not barber:
        return

    message = (
        f'Yangi order keldi: {instance.customer.first_name} {instance.customer.last_name} '
        f'sizni tanladi. U sizning oldingizga {instance.endpoint_time} da kelmoqchi.'
    )
    notify_user(barber.id, message)
