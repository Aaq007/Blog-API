from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (APIOverview, CommentListView, CommentPostView,
                    CommentUpdateView, PostListView, PostUpdateView,
                    UserCreateview, UserListView, UserPasswordChangeView,
                    UserUpdateView)

urlpatterns = [
    path('', APIOverview),

    path("users/", UserListView.as_view()),
    path("users/<int:pk>/", UserUpdateView.as_view()),
    path("users/password-change/", UserPasswordChangeView.as_view()),
    path("usercreate/", UserCreateview.as_view()),

    path('obtain-token/', obtain_auth_token),
    # path('login/', obtain_auth_token),


    path("posts/", PostListView.as_view()),
    path("posts/<int:pk>/", PostUpdateView.as_view()),
    path('posts/<int:pk>/comments/', CommentPostView.as_view()),

    path("comments/", CommentListView.as_view()),
    path("comments/<int:pk>/", CommentUpdateView.as_view()),

]
