import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


# class AddDivisionForm(forms.Form):
#     # Без звя'зування з моделью
#     division_name = forms.CharField(max_length=100, label="Назва підрозділу", required=True)
#     div_abr = forms.CharField(max_length=10, label="Абрівіатура підрозділу", required=True)
#     slug = forms.SlugField(label="URL", required=True)
#     div_description = forms.CharField(label="Опис підрозділу", required=True,
#                                       widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

# У зв'язку з моделью
class AddDivisionForm(forms.ModelForm):
    # для визначення більш конкретних параметрів полів необходіно вказувати їх у констукторі класу
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['division_name'].pattern = "^[А-Яа-яЁё\s]+$"

    class Meta:
        model = Divisions
        fields = ['division_name', 'div_abr', 'div_description']
        widgets = {
            'division_name': forms.Textarea(attrs={'cols': 70, 'rows': 1, }),
        }

    # Створення власного валідатору
    def clean_division_name(self):  # така форма запису обов'язкова clean_поле_форми_до_якого_застосовують
        division_name = self.cleaned_data["division_name"]
        pattern = "^[0-9-А-Яа-яёЁЇїІіЄєҐґ\s]+$"
        if re.match(pattern, division_name) is not None:
            return division_name
        else:
            raise ValidationError('Введені недопустимі символи')


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['division_name', 'slug']

    def clean_fio(self):  # така форма запису обов'язкова clean_поле_форми_до_якого_застосовують
        fio = self.cleaned_data["fio"]
        pattern = "^[0-9-А-Яа-яЇїІіЄєҐґ\s]+$"
        if re.match(pattern, fio) is not None:
            return fio
        else:
            raise ValidationError('Введені недопустимі символи')


class EditInfoPersonForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['tabel', 'division_name', 'oklad', 'phone', 'adress']

    def clean_division_name(self):
        data = self.cleaned_data['division_name']
        # таким образом я сделал вводимые данные в модели Staff объектом класса Divisions
        dn = Divisions()
        dn.division_name = data

        return dn.division_name


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логін користувача"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Підтвердження паролю"

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
