import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.test import Client
from accounts.models import Account
from accounts.jwt_utils import generate_token

user = Account.objects.first()
if not user:
    user = Account.objects.create(username="test_user", role="customer")
tokens = generate_token(user)
access = tokens['access_token']

c = Client(SERVER_NAME='127.0.0.1')
c.cookies['access_token'] = access

response = c.get('/profile/')
print("STATUS:", response.status_code)
if response.status_code == 302:
    print("REDIRECT URL:", response.url)
