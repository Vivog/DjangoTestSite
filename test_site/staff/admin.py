from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.forms.widgets import *
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.
class StaffAdminForm(forms.ModelForm):
    years = []
    for i in range(1930, 2030):
        years.append(i)
    birthday = forms.DateField(label='Дата народження', widget=SelectDateWidget(years=years))

    class Meta:
        model = Staff
        fields = '__all__'

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('div', 'tabel', 'fio', 'get_html_photo',)
    prepopulated_fields = {'slug': ('fio',)}
    list_display_links = ('fio',)
    readonly_fields = ('get_html_photo',)
    # Разбиение подробной информации на секции
    # сначало название секции, потом поля для отображения
    # если название не нужно то пишим None
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('tabel', ('fio', 'slug'), 'prof')}
        ),
        (
            "Додатково", {'fields': ('div', 'oklad', ('birthday', 'phone', 'adress'), 'photo', 'get_html_photo')}
        )
    )
    search_fields = ('tabel', 'fio')
    form = StaffAdminForm

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100")

    get_html_photo.short_description = 'Мініатюра'


