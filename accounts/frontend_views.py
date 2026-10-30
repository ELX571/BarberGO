from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

@login_required
def profile_view(request):
    user = request.user
    
    # Mening e'lonlarim
    my_posts = Post.objects.filter(user=user).order_by('-created_at')
    
    # Yoqqanlar
    # Assuming 'likes' is a ManyToMany on Post to Account
    liked_posts = Post.objects.filter(likes=user).order_by('-created_at')
    
    # Saqlanganlar
    # Assuming 'bookmarks' is a ManyToMany on Post to Account
    # Or maybe there is a Bookmark model?
    # I need to check how bookmarks are implemented.
    
    context = {
        'is_own_profile': True,
        'user': user,
        'my_posts': my_posts,
        'liked_posts': liked_posts,
        'bookmarked_posts': [], # I will check this later
        'profile': {}, # Mock for now
    }
    return render(request, 'profile.html', context)
