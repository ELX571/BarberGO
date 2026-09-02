import re

# Update config/views.py
with open("config/views.py", "r") as f:
    views_content = f.read()

new_view = """
from notifications.models import Notifications

def notifications_view(request):
    logged_in_user = request.user
    
    if not logged_in_user.is_authenticated:
        token = request.COOKIES.get('access_token')
        if token and not blocklisted(token):
            payload, errors = verify_token(token)
            if not errors and payload.get('type') == 'access':
                try:
                    logged_in_user = Account.objects.get(pk=payload['user_id'])
                except Account.DoesNotExist:
                    pass
    
    notifications = []
    if logged_in_user.is_authenticated:
        notifications = Notifications.objects.filter(receptions=logged_in_user).order_by('-created_at')
        
    context = {
        'db_notifications': notifications
    }
    return render(request, 'notifications.html', context)
"""
if "def notifications_view" not in views_content:
    with open("config/views.py", "a") as f:
        f.write("\n" + new_view)

# Update config/urls.py
with open("config/urls.py", "r") as f:
    urls_content = f.read()

urls_content = urls_content.replace(
    "from config.views import profile_view",
    "from config.views import profile_view, notifications_view"
)
urls_content = urls_content.replace(
    "path('notifications/', TemplateView.as_view(template_name='notifications.html'), name='notifications'),",
    "path('notifications/', notifications_view, name='notifications'),"
)
with open("config/urls.py", "w") as f:
    f.write(urls_content)
