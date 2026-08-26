from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'image',
            'video',
            'user',
            'likes_count',
            'is_liked',
            'comments_count',
            'bookmarks_count',
            'is_bookmarked',
            'created_at',
            'updated_at'
        )

    def get_user(self, obj):
        from accounts.serializers import UserSerializer
        return UserSerializer(obj.user, context=self.context).data if obj.user else None

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
        
    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(id=request.user.id).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'image',
            'video',
            'user',
            'created_at'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'image': {'required': False, 'allow_null': True},
            'video': {'required': False, 'allow_null': True},
        }


class PostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title',
            'description',
            'image',
            'video',
        )
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'video': {'required': False, 'allow_null': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username', read_only=True)

    def comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Comment
        fields = (
            'id',
            'username',
            'text',
            'created_at',
        )

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
