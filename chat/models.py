from django.db import models
from accounts.models import Account
from base.models import BaseModel


class Room(BaseModel):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='room')
