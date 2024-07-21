from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm)

from users.models import UserModel


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
            'class': "form-control py-4",
            'placeholder': 'Введите имя пользователя',
        }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': "form-control py-4",
            'placeholder': 'Введите пароль',
        }))

    class Meta:
        model = UserModel
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите фамилию',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите логин',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите адрес эл. почты',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Введите пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': 'Подтвердите пароль',
    }))

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
