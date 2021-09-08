from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Comment, Post, User
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from .serializers import (CommentCreateSerializer, CommentPostSerializer,
                          CommentSerializer, PostCreateSerializer,
                          PostSerializer, UserPasswordChangeSerializer,
                          UserRegisterSerializer, UserSerializer)

# Create your views here.


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def APIOverview(request):
    return Response({'Hello': 'world'})


class UserListView(generics.ListAPIView):
    """List all users, Only admin can access"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    authentication_classes = [TokenAuthentication]


class UserPasswordChangeView(generics.UpdateAPIView):
    """View for changing the password of auhtorized user"""
    serializer_class = UserPasswordChangeSerializer
    queryset = User.objects.all()
    permission_classes = (IsUserOrReadOnly,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(data={'password changed': 'Successful'}, status=status.HTTP_200_OK)


# @api_view(['PATCH', 'PUT'])
# @permission_classes([IsUserOrReadOnly])
# def UserProfileEdit(request, *args, **kwargs):
#     print(request.user)
#     user = User.objects.get(id=request.user.id)
#     if user:
#         serializer = UserSerializer(
#             user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data='Success')
#     return Response('Not success')


class UserCreateview(generics.CreateAPIView):
    """View for registering new user"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user=response.data['id'])
        return Response(({token.key}))


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """View for get,update, patch and delete user instance"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class PostListView(generics.ListCreateAPIView):
    """View for get all the post and create new post"""
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        else:
            return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class PostUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Get,update,patch or delete post instance. Only avalible to post author"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class CommentListView(generics.ListCreateAPIView):
    """Create and get comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('post', 'user')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """get,update,patch and delete comment instance, Only avaliable to comment author"""
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class CommentPostView(generics.ListAPIView):
    """Get comments that belongs to user"""
    serializer_class = CommentPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        return Post.objects.get(id=self.kwargs.get('pk'))

    def get_queryset(self):
        post = self.get_object()
        return Comment.objects.filter(post=post)
