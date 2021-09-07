from dataclasses import field
from .models import User, Post, Comment
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_id', 'name', 'email']

    # def save(self, **kwargs):
    #     user = self.context['request'].user
    #     user.user_id = self.validated_data['user_id']
    #     user.name = self.validated_data['name']
    #     user.email = self.validated_data['email']

    #     user.save()
    #     return user

    # def update(self, instance, validated_data):
    #     print('Update from serialzier')
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.user_id = validated_data.get('user_id', instance.user_id)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    # class Meta:
    #     model = User
    #     fields = ['old_password', 'new_password1', 'new_password2']

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
        # password_validation.validate_password(
        #     attrs['new_password1'], self.context['request'].user)
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        password = self.validated_data['new_password1']
        user.set_password(password)
        user.save()
        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'user_id', 'name', 'email', 'password']
        # extra_kwargs = {'password': {'write_only=True'}}

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


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('comment', 'post', 'user')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)
