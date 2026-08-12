from celery import shared_task
from django.core.mail import send_mail

# from accounts.views import full_name
from config import settings

@shared_task
def welcome_email(email,first_name,last_name):
    subject = f'Welcome Message'
    message= f'Hi {last_name} {first_name} welcome to our BarberGo web site'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return f'{email}ga maktub yubordik'

@shared_task
def verification_code(code,username,email):
    subject = f'Verification Code'
    message=f'Welcome back {username} your verification code: {code}'
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,

    )


