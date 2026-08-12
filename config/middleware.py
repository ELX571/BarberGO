import urllib.parse
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from accounts.jwt_utils import verify_token

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        payload, error = verify_token(token_key)
        if error or payload.get('type') != 'access':
            return AnonymousUser()
        user_id = payload['user_id']
        return User.objects.get(id=user_id)
    except Exception:
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = urllib.parse.parse_qs(query_string)

        token = query_params.get("token", [None])[0]

        # Agar URL'da token bo'lmasa, Headerdan (Authorization: Bearer <token>) qidiramiz
        if not token:
            for name, value in scope.get("headers", []):
                if name == b"authorization":
                    auth_header = value.decode()
                    if auth_header.startswith("Bearer "):
                        token = auth_header.split(" ")[1]
                    break

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)
