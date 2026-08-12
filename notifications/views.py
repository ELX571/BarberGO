from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
         f'notifications.{user_id}',
        {
            'type': 'send_notification',
            'message': message
        }
    )
