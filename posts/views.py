from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.query_utils import Q
from drf_yasg.utils import swagger_auto_schema
from django.db.models import BooleanField, Case, Value, When
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.authtications import JwtAuthentication
from posts.models import Post, Comment
from posts.serializers import PostCreateSerializer, PostDetailsSerializer, CommentSerializer, CommentCreateSerializer, \
    PostSerializer


class Posts(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        if self.action in ['update', 'partial_update', 'retrieve']:
            return PostDetailsSerializer
        return PostSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        posts = Post.objects.all()

        if search:
            posts = posts.annotate(
                similarity_title=TrigramSimilarity('title', search),
                similarity_description=TrigramSimilarity('description', search),
                similarity_user=TrigramSimilarity('user', search),

            ).filter(Q(similarity_title__gt=0.3) | Q(similarity_description__gt=0.3) | Q(similarity_user__gt=0.3)).order_by('-created_at')

            return posts



    def list(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Faqat barberlar post yarata oladi
        if getattr(request.user, 'role', None) != 'barber':
            return Response(
                {'error': 'Faqat barberlar post yarata oladi'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        post = Post.objects.get(id=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'error': 'Siz bu postni tahrirlay olmaysiz'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'error': 'Siz bu postni tahrirlay olmaysiz'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({'error': 'Siz bu postni o\'chira olmaysiz'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='like', permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            like = False
        else:
            post.likes.add(request.user)
            like = True
        return Response({
            'like': like,
            'likes': post.likes.count()
        })

    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        responses={201: CommentCreateSerializer},
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = self.get_object()

        comment = Comment.objects.create(
            user=request.user,
            parent_post=post,
            text=serializer.validated_data["text"]
        )

        return Response({
            "message": "Comment qo'shildi",
            "comment": CommentSerializer(comment).data,
            "comments_count": post.comments.count()
        })

    @action(detail=True, methods=['get'], url_path='get_comment', permission_classes=[IsAuthenticated])
    def get_comment(self, request, pk=None):
        post = self.get_object()

        comment = post.comments.all()

        serializer = CommentSerializer(comment, many=True)

        return Response(serializer.data)


class RecommendedPostViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_region = user.city

        return (
            Post.objects
            .annotate(
                is_local=Case(
                    When(user__city=user_region, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .order_by('-is_local', '-created_at')
        )
