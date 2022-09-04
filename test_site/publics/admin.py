from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import *


# Register your models here.



class PublicationsAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст публікації', widget=CKEditorUploadingWidget())

    class Meta:
        model = Publications
        fields = '__all__'

class ReviewPubsInline(admin.TabularInline):
    model = ReviewsPubs
    extra = 1
    readonly_fields = ('name', 'email')


@admin.register(Publications)
class PublicationsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('name', 'div', "display_author", 'file_load')
    list_filter = ('div',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    form = PublicationsAdminForm
    save_on_top = True
    inlines = [ReviewPubsInline]


@admin.register(ReviewsPubs)
class ReviewPubsAdmin(admin.ModelAdmin):
    """Відгуки до публікації"""
    list_display = ("name", "email", "parent", "pub")
    readonly_fields = ("name", "email")