import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.test import Client
c = Client(SERVER_NAME='127.0.0.1')
try:
    response = c.get('/profile/')
    print("STATUS:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
