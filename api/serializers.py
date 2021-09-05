from .models import User, Post, Comment
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_id', 'name', 'email']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'user_id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only=True'}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):

    post_comments = serializers.StringRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'topic', 'content', 'user', 'post_comments')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    post = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ('comment', 'post', 'get_post', 'user')
