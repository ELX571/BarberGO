from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

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
            'created_at',
            'updated_at'
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
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
