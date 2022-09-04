from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import *
# Register your models here.


class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст новини', widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    form = NewsAdminForm


@admin.register(ReviewsNews)
class ReviewNewsAdmin(admin.ModelAdmin):
    """Відгуки до новини"""
    list_display = ("name", "email", "parent", "news")
    readonly_fields = ("name", "email")


