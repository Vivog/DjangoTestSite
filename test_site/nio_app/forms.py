from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class ReviewPubForm(forms.ModelForm):
    class Meta:
        model = ReviewsPubs
        fields = ('name', 'email', 'text')


class ReviewNewsForm(forms.ModelForm):
    class Meta:
        model = ReviewsNews
        fields = ('name', 'email', 'text')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Логін",
                                               'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Пошта"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Пароль(ще раз)"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Логін",
                                               'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Пароль"}))
