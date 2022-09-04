from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.


@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('abr', 'boss', 'staff',)
    list_display_links = ('abr',)
    prepopulated_fields = {'slug': ('abr',), }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['num_staff'].initial = 0
        form.base_fields['num_projects'].initial = 0
        form.base_fields['num_docs'].initial = 0
        return form

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('loc',)


@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Theses)
class ThesesAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_html_photo')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50")

    get_html_photo.short_description = 'Мініатюра'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# Изменяет название страницы административной панели и название заголовка административной панали
admin.site.site_title = "Портал НДВ"
admin.site.site_header = "Портал НДВ"
