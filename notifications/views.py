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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notifications

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_notifications(request):
    notifs = Notifications.objects.filter(receptions=request.user).order_by('-created_at')
    data = []
    for n in notifs:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.description,
            'time': n.created_at.isoformat(),
            'read': False
        })
    return Response(data)
