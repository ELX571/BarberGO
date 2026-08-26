from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post

from accounts.jwt_utils import verify_token, blocklisted
from accounts.models import Account

def profile_view(request, user_id=None):
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
    
    if user_id:
        target_user = get_object_or_404(Account, id=user_id)
        is_own_profile = (logged_in_user.is_authenticated and logged_in_user.id == target_user.id)
    else:
        target_user = logged_in_user
        is_own_profile = True
        
    if target_user.is_authenticated or user_id:
        my_posts = Post.objects.filter(user=target_user).order_by('-created_at')
        liked_posts = Post.objects.filter(likes=target_user).order_by('-created_at') if is_own_profile else []
        bookmarked_posts = Post.objects.filter(bookmarks=target_user).order_by('-created_at') if is_own_profile else []
    else:
        my_posts = []
        liked_posts = []
        bookmarked_posts = []
        
    context = {
        'is_own_profile': is_own_profile,
        'is_authenticated': logged_in_user.is_authenticated,
        'user': target_user,
        'my_posts': my_posts,
        'liked_posts': liked_posts,
        'bookmarked_posts': bookmarked_posts,
        'profile': {},
    }
    return render(request, 'profile.html', context)
