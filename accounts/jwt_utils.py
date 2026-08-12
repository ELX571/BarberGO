from datetime import datetime, timedelta, timezone

import jwt

from config import settings


def generate_token(user):
    access_payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp' : datetime.now(timezone.utc) + timedelta(minutes=60),
        'type': 'access',

    }

    refresh_payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'type': 'refresh',

    }


    access_token = jwt.encode(access_payload,settings.SECRET_KEY,algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload,settings.SECRET_KEY,algorithm='HS256')
    return {'access_token': access_token, 'refresh_token': refresh_token}

def verify_token(token):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        return payload,None
    except jwt.ExpiredSignatureError:
        return None,'token muddati otgan'
    except jwt.InvalidTokenError:
        return None,'token invalid(xato)'



def blocklisted(token):
    from accounts.models import BlocklistedToken
    return BlocklistedToken.objects.filter(token=token).exists()

