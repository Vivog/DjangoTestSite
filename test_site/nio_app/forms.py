import re

from django import forms
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
        fields = ['division_name', 'div_abr', 'slug', 'div_description']
        widgets = {
            'division_name': forms.Textarea(attrs={'cols': 70, 'rows': 1, }),
        }

    # Створення власного валідатору
    def clean_division_name(self):  # така форма запису обов'язкова clean_поле_форми_до_якого_застосовують
        division_name = self.cleaned_data["division_name"]
        pattern = "^[А-Яа-яЁё\s]+$"
        if re.match(pattern, division_name) is not None:
            return division_name
        else:
            raise ValidationError('Введені недопустимі символи')
