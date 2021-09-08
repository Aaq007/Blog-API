from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Custom User Manager for Custome User mdoel"""

    def create_user(self, user_id, password, name=None, email=None, **kwargs):
        if not user_id:
            raise ValueError('User must have valid user ID')

        user = self.model(user_id=user_id, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, name=None, email=None,  **kwargs):
        user = self.create_user(
            user_id=user_id, password=password, name=name, email=email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_id, password, name=None, email=None,  **kwargs):
        user = self.create_user(
            user_id=user_id, password=password, name=name, email=email)
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    """Custom User model that identifies user by User ID"""
    user_id = models.CharField(
        verbose_name='User ID', unique=True, max_length=32)
    name = models.CharField(verbose_name='User name',
                            max_length=255, null=True, blank=True)
    email = models.EmailField(
        max_length=255, verbose_name='Email address', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name

    def __str__(self):
        return self.user_id

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_staff


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


class Post(models.Model):
    topic = models.CharField(verbose_name='Post topic', max_length=255)
    user = models.ForeignKey(
        User, verbose_name='Post author', on_delete=models.CASCADE, related_name='post_user')
    content = models.CharField(verbose_name='Post content', max_length=255)

    def __str__(self):
        return self.topic

    @property
    def comment_count(self):
        return self.post_comments.count()

    @property
    def post_user(self):
        return self.user.user_id

    @property
    def post_comments(self):
        return f"{self.post_comments.user}"


class Comment(models.Model):
    comment = models.CharField(
        verbose_name='Comment', max_length=255)
    post = models.ForeignKey(Post, verbose_name='Post', related_name='post_comments',
                             on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_user')

    def __str__(self) -> str:
        return self.comment

    @property
    def comment_user(self):
        return self.user.user_id
