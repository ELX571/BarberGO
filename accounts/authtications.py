from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from accounts.jwt_utils import blocklisted, verify_token
from accounts.models import Account

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ', 1)[1]
        if blocklisted(token):
            raise exceptions.AuthenticationFailed('Token is blocklisted')
        payload, errors = verify_token(token)
        if errors:
            raise exceptions.AuthenticationFailed(errors)
        if payload.get('type') != 'access':
            raise exceptions.AuthenticationFailed('Notogri token turi')

        try:
            user = Account.objects.get(pk=payload['user_id'])
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed('Bunday user topilmadi')
        return user, token
