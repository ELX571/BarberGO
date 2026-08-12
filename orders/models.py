from django.db import models

from accounts.models import Account
from base.models import BaseModel


class Order(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending','Pending'
        ACCEPTED = "accepted", "Accepted"
        CANCELED = "canceled", "Canceled"

    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='customer_orders')
    barber= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='barber_orders')
    status = models.CharField(choices=Status.choices, default=Status.PENDING, max_length=10)
    description = models.TextField()
    image = models.ImageField(upload_to='media/style', blank=True, null=True)
    endpoint_time = models.DateTimeField()

