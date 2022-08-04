from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('abr', 'boss', 'staff',)
    prepopulated_fields = {'slug': ('abr',), }

    # prepopulated_fields = {'slug': ('abr',), 'num_staff': ('staff',), 'num_projects': ('projects',), 'num_docs': ('docs',)}
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['num_staff'].initial = 0
        form.base_fields['num_projects'].initial = 0
        form.base_fields['num_docs'].initial = 0
        return form


@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ('abr', 'boss', 'num_staff', 'get_html_photo')
    prepopulated_fields = {'slug': ('abr',)}
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('name', 'abr', 'slug', 'description')}
        ),
        (
            "Додатково", {'fields': ('num_staff', 'num_docs', 'num_projects', 'locs', 'coops', 'theses', )}
        ),
        (
            'Управління', {'fields': ('boss', 'photo')}
        )
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['num_staff'].initial = 0
        form.base_fields['num_projects'].initial = 0
        form.base_fields['num_docs'].initial = 0
        return form

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50")

    get_html_photo.short_description = 'Мініатюра'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('div', 'tabel', 'fio', 'get_html_photo',)
    prepopulated_fields = {'slug': ('fio',)}
    # Разбиение подробной информации на секции
    # сначало название секции, потом поля для отображения
    # если название не нужно то пишим None
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('tabel', 'fio', 'slug', 'prof')}
        ),
        (
            "Додатково", {'fields': ('div', 'oklad', 'birthday', 'phone', 'adress', 'photo')}
        )
    )
    search_fields = ('tabel', 'fio')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50")

    get_html_photo.short_description = 'Мініатюра'


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('div', 'release_date', "status", "type", "name", "display_author", 'file_load')
    list_filter = ('div', 'status', 'type')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('loc',)


@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('name', 'div', "display_author", 'file_load')
    list_filter = ('div',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Publications)
class PublicationsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('name', 'div', "display_author", 'file_load')
    list_filter = ('div',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

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
    list_display = ('name', )
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# Изменяет название страницы административной панели и название заголовка административной панали
admin.site.site_title = "Портал НДВ"
admin.site.site_header = "Портал НДВ"
