import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from config.middleware import JWTAuthMiddleware
import notifications.routing
import chat.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns +
            chat.routing.websocket_urlpatterns
        )
    )
})
