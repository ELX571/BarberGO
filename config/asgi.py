import os

"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from config.middleware import JWTAuthMiddleware
import notifications.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    )
})
