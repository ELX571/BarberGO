import re

# Update notifications/views.py to add an API endpoint
with open("notifications/views.py", "a") as f:
    f.write("""
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
""")

# Create notifications/urls.py
with open("notifications/urls.py", "w") as f:
    f.write("""
from django.urls import path
from notifications.views import get_user_notifications

urlpatterns = [
    path('api/', get_user_notifications, name='get_user_notifications'),
]
""")

# Include it in config/urls.py
with open("config/urls.py", "r") as f:
    content = f.read()

if "path('notifications/', include('notifications.urls'))" not in content:
    content = content.replace(
        "path('orders/', include('orders.urls')),",
        "path('orders/', include('orders.urls')),\n    path('notifications/', include('notifications.urls')),"
    )
    with open("config/urls.py", "w") as f:
        f.write(content)

