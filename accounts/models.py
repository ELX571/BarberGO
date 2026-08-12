import datetime
import random


from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils import timezone

from base.models import BaseModel


class Account(AbstractUser):
    Role_CHOICES = (
        ("barber", "Barber"),
        ("customer", "Customer"),
    )
    REGION_CHOICES = (
        ('tashkent_sh', 'Toshkent shahri'),
        ('tashkent_v', 'Toshkent viloyati'),
        ('andijan', 'Andijon viloyati'),
        ('bukhara', 'Buxoro viloyati'),
        ('fergana', "Farg'ona viloyati"),
        ('jizzakh', 'Jizzax viloyati'),
        ('namangan', 'Namangan viloyati'),
        ('navoiy', 'Navoiy viloyati'),
        ('kashkadarya', 'Qashqadaryo viloyati'),
        ('samarkand', 'Samarkand viloyati'),
        ('sirdaryo', 'Sirdaryo viloyati'),
        ('surxondaryo', 'Surxondaryo viloyati'),
        ('khorezm', 'Xorazm viloyati'),
        ('karakalpakstan', "Qoraqalpog'iston Respublikasi"),
    )
    role = models.CharField(max_length=10, choices=Role_CHOICES)
    avatar = models.ImageField(upload_to="media/avatars", default="media/avatars/default.jpg")
    phone_number = models.CharField(max_length=17, default="+998")
    city=models.CharField(max_length=50, default="tashkent_sh",choices=REGION_CHOICES)


class BlocklistedToken(models.Model):
    token = models.TextField( unique=True)
    blocklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f'blocklisted_at: {self.blocklisted_at}'


def generate_code():
    return random.randint(100000, 999999)

def exp_time():
    return timezone.now() + datetime.timedelta(minutes=2)

class VerificationCode(BaseModel):
    user=models.ForeignKey(Account, on_delete=models.CASCADE,related_name='verification_code')
    code = PositiveIntegerField(default=generate_code)
    expired_at = models.DateTimeField(default=exp_time)

    def is_valid(self):
        return timezone.now() < self.expired_at

    def __str__(self):
        return f'{self.user.username} Verification Code: {self.code}'


