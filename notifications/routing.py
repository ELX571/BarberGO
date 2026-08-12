from django.urls import re_path

from notifications import consumer

websocket_urlpatterns = [
       re_path(
           r'ws/notifications/$',
           consumer.NotificationsConsumer.as_asgi()
       )
]