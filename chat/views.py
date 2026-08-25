from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from orders.models import Order
from .models import ChatRoom
from .serializers import MessageSerializer


def chat_page(request, order_id=None):
    """Bitta sahifa: chapda ro'yxat, o'ngda faol suhbat. order_id bo'lsa avtomatik ochiladi."""
    return render(request, 'chat.html', {'order_id': order_id})


class ChatHistoryView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs['order_id'])
        if self.request.user.id not in (order.customer_id, order.barber_id):
            raise PermissionDenied("Bu suhbatga kirish huquqingiz yo'q.")
        room, _ = ChatRoom.objects.get_or_create(order=order)
        # sahifa ochilganda, o'zganing yozgan xabarlarini "o'qilgan" deb belgilaymiz
        room.messages.exclude(sender=self.request.user).update(is_read=True)
        return room.messages.select_related('sender').all()


class MyChatRoomsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            Q(order__customer_id=user.id) | Q(order__barber_id=user.id)
        ).select_related('order', 'order__customer', 'order__barber')

    def list(self, request, *args, **kwargs):
        user = request.user
        data = []
        for room in self.get_queryset():
            order = room.order
            other = order.barber if order.customer_id == user.id else order.customer
            last_msg = room.messages.order_by('-created_at').first()
            unread = room.messages.filter(is_read=False).exclude(sender=user).count()
            data.append({
                'order_id': room.order_id,
                'other_user_id': other.id,
                'other_user_name': other.username,
                'last_message': last_msg.text if last_msg else None,
                'last_message_time': last_msg.created_at.isoformat() if last_msg else None,
                'unread_count': unread,
            })
        return Response(data)

