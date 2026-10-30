from django.db import models

from base.models import BaseModel
from config import settings


class Notifications(BaseModel):
    title = models.TextField()
    description = models.TextField()
    receptions = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='notifications')
    order_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

