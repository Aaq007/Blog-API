from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

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
        return super().has_perm(perm, obj=obj)

    def has_module_perms(self, app_label: str) -> bool:
        return super().has_module_perms(app_label)


class Post(models.Model):
    topic = models.CharField(verbose_name='Post topic', max_length=255)
    user = models.ForeignKey(
        User, verbose_name='Post author', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='Post content', max_length=255)

    def __str__(self):
        return self.topic


class Comment(models.Model):
    comment = models.CharField(
        verbose_name='Comment', max_length=255)
    post = models.ForeignKey(Post, verbose_name='Post',
                             on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment
