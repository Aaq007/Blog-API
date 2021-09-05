from django.shortcuts import render
from django.views import View

from .serializers import CommentSerializer, UserSerializer, PostSerializer
from .models import User, Post, Comment

from rest_framework import generics
from rest_framework.viewsets import ViewSet
# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserRetrieveView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserCreateview(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
