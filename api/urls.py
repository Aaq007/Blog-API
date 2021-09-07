from django.urls import path, include, re_path
from .views import (APIOverview, CommentListView, CommentUpdateView, PostUpdateView, UserCreateview,
                    UserListView, PostListView, UserPasswordChangeView, UserProfileEdit, UserUpdateView)

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

# router.register('users/', UserListView, basename='users')
# router.register('posts/', PostListView, 'posts')

urlpatterns = [
    # path('', include(router.urls))
    path('', APIOverview),

    path("users/", UserListView.as_view()),
    path("users/<int:pk>/", UserUpdateView.as_view()),
    path("users/password-change/", UserPasswordChangeView.as_view()),
    path("usercreate/", UserCreateview.as_view()),

    path('obtain-token/', obtain_auth_token),

    # path('profile/<int:pk>/', UserProfileView.as_view()),
    # path('profile/<int:pk>/', UserProfileEdit),

    path("posts/", PostListView.as_view()),
    path("posts/<int:pk>/", PostUpdateView.as_view()),
    # re_path("posts/?<str:username>/", PostListView.as_view()),

    path("comments/", CommentListView.as_view()),
    path("comments/<int:pk>/", CommentUpdateView.as_view()),

]
