from django.shortcuts import render

from .serializers import UserSerializer
from .models import User, Post

from rest_framework import generics
# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
