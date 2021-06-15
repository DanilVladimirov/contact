from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from contact.models import User, Post, PageUsers, ImagesUser, Public
from django import forms


class MyUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserNameSurname(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['label', 'text']


class UserSettings(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class ImageUser(ModelForm):
    class Meta:
        model = PageUsers
        fields = ['logo']


class BackGroundUser(ModelForm):
    class Meta:
        model = PageUsers
        fields = ['background']


class UploadImageForm(ModelForm):
    class Meta:
        model = ImagesUser
        fields = '__all__'


class UploadLogoPublicForm(ModelForm):
    class Meta:
        model = Public
        fields = ['logo']


class UploadBackPublicForm(ModelForm):
    class Meta:
        model = Public
        fields = ['background']


class InfoPublicForm(ModelForm):
    class Meta:
        model = Public
        fields = ['title', 'desc']


class CreatePublicForm(ModelForm):
    class Meta:
        model = Public
        fields = ['title', 'desc', 'logo', 'background']
