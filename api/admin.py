from dataclasses import field
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
# admin.site.register(User)
# admin.site.register(UserAdmin)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'password',
                  'email', 'is_active', 'is_staff')

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValueError('Password do not match')
        return password1

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('user_id', 'name', 'password',
                  'email', 'is_active', 'is_staff')


class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('user_id', 'email',  'is_staff')
    list_filter = ('user_id',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id',  'password1', 'password2'),
        }),
    )
    search_fields = ('user_id',)
    ordering = ('id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)

# admin.site.unregister(Group)
