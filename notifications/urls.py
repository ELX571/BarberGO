
from django.urls import path
from notifications.views import get_user_notifications

urlpatterns = [
    path('api/', get_user_notifications, name='get_user_notifications'),
]
