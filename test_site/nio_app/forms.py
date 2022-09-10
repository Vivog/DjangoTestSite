from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Логін",
                                               'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "Пошта"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я",
                                               'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Призвіще",
                                               'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Пароль (ще раз)"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Логін",
                                               'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Пароль",
                                                                 'readonly':True, 'onfocus': "this.removeAttribute('readonly')"}))
