from django.db import models
from accounts.models import Account
from base.models import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    likes = models.ManyToManyField(Account, related_name='liked_post', blank=True)
    video = models.FileField(upload_to='media/posts/videos', blank=True, null=True)
    image = models.ImageField(upload_to='media/posts/images', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()


class Comment(BaseModel):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user} - {self.parent_post}"
