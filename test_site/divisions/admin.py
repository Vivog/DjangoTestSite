from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.
class DivisionsAdminForm(forms.ModelForm):
    description = forms.CharField(label='Опис підрозділу', widget=CKEditorUploadingWidget())

    class Meta:
        model = Divisions
        fields = '__all__'

@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ('main_div', 'abr',)
    list_display_links = ('abr',)
    prepopulated_fields = {'slug': ('abr',)}
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('name', ('abr', 'slug'), 'main_div', 'description')}
        ),
        (
            "Додатково", {'fields': (('locs', 'coops', 'theses',),)}
        ),
        (
            'Додаткові фото', {'fields': ('pics',)}
        ),
    )
    form = DivisionsAdminForm
    search_fields = ('main_div', 'abr')



@admin.register(DivisionsPics)
class DivisionsPicsAdmin(admin.ModelAdmin):
    list_display = ('pic', 'get_html_photo')

    def get_html_photo(self, object):
        if object.pic:
            return mark_safe(f"<img src='{object.pic.url}' width=100")

    get_html_photo.short_description = 'Мініатюра'