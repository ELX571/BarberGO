import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.test import Client
from accounts.models import Account
from rest_framework_simplejwt.tokens import RefreshToken

user = Account.objects.first()
if not user:
    print("No users found")
    exit(0)
    
refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)

c = Client()
# Do NOT force_login, just set the cookie
c.cookies['access_token'] = access_token

response = c.get(f'/chat/start/{user.id}/', HTTP_HOST='127.0.0.1:8000')
print("STATUS TO SAME USER:", response.status_code, response.url if response.status_code == 302 else '')

other_user = Account.objects.exclude(id=user.id).first()
if other_user:
    response = c.get(f'/chat/start/{other_user.id}/', HTTP_HOST='127.0.0.1:8000')
    print("STATUS TO OTHER USER:", response.status_code, response.url if response.status_code == 302 else '')
