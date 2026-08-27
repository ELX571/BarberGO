import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chat.models import ChatRoom
from django.db.models import Q
qs = ChatRoom.objects.all()
print("All rooms:", qs.count())
