from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.forms.widgets import *
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.
class DocumentsAdminForm(forms.ModelForm):
    years = []
    for i in range(1990, 2051):
        years.append(i)
    description = forms.CharField(label='Опис документу', widget=CKEditorUploadingWidget())
    release_date = forms.DateField(label='Дата впровадження', widget=SelectDateWidget(years=years))

    class Meta:
        model = Documents
        fields = '__all__'

@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('number', 'div', 'release_date', "status", "type", "name", "display_author", 'file_load')
    list_display_links = ('name',)
    list_filter = ('div', 'status', 'type')
    search_fields = ('name', 'year', 'type')
    prepopulated_fields = {'slug': ('name',), }
    form = DocumentsAdminForm