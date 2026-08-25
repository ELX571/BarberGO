from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

from accounts.jwt_utils import verify_token, blocklisted
from accounts.models import Account

def profile_view(request):
    user = request.user
    
    if not user.is_authenticated:
        token = request.COOKIES.get('access_token')
        if token and not blocklisted(token):
            payload, errors = verify_token(token)
            if not errors and payload.get('type') == 'access':
                try:
                    user = Account.objects.get(pk=payload['user_id'])
                except Account.DoesNotExist:
                    pass
    
    if user.is_authenticated:
        my_posts = Post.objects.filter(user=user).order_by('-created_at')
        liked_posts = Post.objects.filter(likes=user).order_by('-created_at')
        is_own_profile = True
    else:
        my_posts = []
        liked_posts = []
        is_own_profile = False
        
    context = {
        'is_own_profile': is_own_profile,
        'user': user,
        'my_posts': my_posts,
        'liked_posts': liked_posts,
        'bookmarked_posts': [],
        'profile': {},
    }
    return render(request, 'profile.html', context)
