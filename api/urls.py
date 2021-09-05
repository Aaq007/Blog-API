from django.urls import path, include
from .views import CommentListView, UserCreateview, UserListView, PostListView, UserUpdateView

from rest_framework import routers

router = routers.DefaultRouter()

# router.register('users/', UserListView, basename='users')
# router.register('posts/', PostListView, 'posts')

urlpatterns = [
    # path('', include(router.urls))
    path("users/", UserListView.as_view()),
    path("users/<int:pk>", UserUpdateView.as_view()),
    path("usercreate/", UserCreateview.as_view()),
    path("posts/", PostListView.as_view()),
    path("comments/", CommentListView.as_view()),

]
