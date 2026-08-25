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
        qs = ChatRoom.objects.filter(
            Q(order__customer_id=user.id) | Q(order__barber_id=user.id)
        ).select_related('order', 'order__customer', 'order__barber')
        
        q = self.request.query_params.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(order__id__icontains=q) |
                Q(order__customer__username__icontains=q) |
                Q(order__barber__username__icontains=q) |
                Q(order__customer__first_name__icontains=q) |
                Q(order__customer__last_name__icontains=q) |
                Q(order__barber__first_name__icontains=q) |
                Q(order__barber__last_name__icontains=q)
            )
        return qs

    def list(self, request, *args, **kwargs):
        user = request.user
        data = []
        for room in self.get_queryset():
            order = room.order
            other = order.barber if order.customer_id == user.id else order.customer
            
            # Agar foydalanuvchida ism-familiya kiritilgan bo'lsa, shuni ko'rsatamiz, 
            # yo'qsa username ko'rsatamiz.
            other_name = f"{other.first_name} {other.last_name}".strip()
            if not other_name:
                other_name = other.username
                
            last_msg = room.messages.order_by('-created_at').first()
            unread = room.messages.filter(is_read=False).exclude(sender=user).count()
            data.append({
                'order_id': room.order_id,
                'other_user_id': other.id,
                'other_user_name': other_name,
                'last_message': last_msg.text if last_msg else None,
                'last_message_time': last_msg.created_at.isoformat() if last_msg else None,
                'unread_count': unread,
            })
        return Response(data)


from rest_framework.parsers import MultiPartParser, FormParser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ChatMessageUploadView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        order_id = self.kwargs['order_id']
        order = Order.objects.get(id=order_id)
        if self.request.user.id not in (order.customer_id, order.barber_id):
            raise PermissionDenied("Sizda bu chatga yozish huquqi yo'q.")
        
        room, _ = ChatRoom.objects.get_or_create(order=order)
        message = serializer.save(room=room, sender=self.request.user)

        channel_layer = get_channel_layer()
        group_name = f'chat_{order_id}'
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message_id': message.id,
                'sender_id': message.sender.id,
                'sender_name': message.sender.username,
                'text': message.text,
                'image': message.image.url if message.image else None,
                'video': message.video.url if message.video else None,
                'voice': message.voice.url if message.voice else None,
                'created_at': message.created_at.isoformat(),
            }
        )
