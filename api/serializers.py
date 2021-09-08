from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Comment, Post, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_id', 'name', 'email']


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password is incorrect!'))
        return value

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {'new_password2': _('Password do not match')})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        password = self.validated_data['new_password1']
        user.set_password(password)
        user.save()
        return user


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_id', 'name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):

    post_comments = serializers.StringRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'topic', 'content', 'user',
                  'post_comments', 'comment_count', 'post_user')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('topic', 'content')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment', 'post', 'user')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user', 'id')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CommentPostSerializer(serializers.Serializer):
    comment = serializers.CharField(read_only=True)
    post = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
