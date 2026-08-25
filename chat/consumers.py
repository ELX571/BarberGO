import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatRoom, Message
from orders.models import Order


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_{self.order_id}'
        self.user = self.scope['user']

        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        if not await self.user_has_access():
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        text = (data.get('message') or '').strip()
        if not text:
            return

        message = await self.save_message(text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': message.id,
                'sender_id': self.user.id,
                'sender_name': self.user.username,
                'text': text,
                'created_at': message.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message_id': event['message_id'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'text': event['text'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def user_has_access(self) -> bool:
        try:
            order = Order.objects.get(id=self.order_id)
        except Order.DoesNotExist:
            return False
        return self.user.id in (order.customer_id, order.barber_id)

    @database_sync_to_async
    def save_message(self, text: str) -> Message:
        room, _ = ChatRoom.objects.get_or_create(order_id=self.order_id)
        return Message.objects.create(room=room, sender=self.user, text=text)
