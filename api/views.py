from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .models import Comment, Post, User
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from .serializers import (CommentCreateSerializer, CommentSerializer,
                          PostCreateSerializer, PostSerializer,
                          UserPasswordChangeSerializer, UserRegisterSerializer,
                          UserSerializer)

# Create your views here.


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def APIOverview(request):
    return Response({'Hello'})


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    authentication_classes = [TokenAuthentication]


class UserPasswordChangeView(generics.UpdateAPIView):
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


@api_view(['PATCH', 'PUT'])
@permission_classes([IsUserOrReadOnly])
def UserProfileEdit(request, *args, **kwargs):
    print(request.user)
    user = User.objects.get(id=request.user.id)
    if user:
        serializer = UserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data='Success')
    # else:
    #     return Response('Only for registered users')
    return Response('Not success')


class UserCreateview(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success'}, status=status.HTTP_201_CREATED)


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class PostListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        if self.request.method == 'POST':
            return Post.objects.filter(user=self.request.user)
        else:
            return Post.objects.all()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class PostUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class CommentListView(generics.ListCreateAPIView):
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
        return serializer.save(user=self.request.user)
    # def per


class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)
