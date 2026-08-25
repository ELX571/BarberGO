from django.db import models

from accounts.models import Account
from orders.models import Order


class ChatRoom(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='chat_room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat room #{self.id} (order #{self.order_id})"

    def is_participant(self, user) -> bool:
        return user.id in (self.order.customer_id, self.order.barber_id)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_chat_messages')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/chat', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_id}: {(self.text or '[rasm]')[:30]}"

