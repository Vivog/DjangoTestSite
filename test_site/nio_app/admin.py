from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('abr', 'boss', 'num_staff', 'divisions')
    prepopulated_fields = {'slug': ('abr',), 'num_staff': ('staff',), 'num_projects': ('projects',), 'num_docs': ('docs',)}



@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ('abr', 'num_staff', )
    prepopulated_fields = {'slug': ('div_abr',)}


class StaffAdmin(admin.ModelAdmin):
    list_display = ('tabel', 'fio', 'get_html_photo')
    list_display_links = ('tabel', 'fio')
    list_filter = ('division_name',)
    prepopulated_fields = {'slug': ('fio',)}
    # Разбиение подробной информации на секции
    # сначало название секции, потом поля для отображения
    # если название не нужно то пишим None
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('tabel', 'fio', 'slug', 'prof')}
        ),
        (
            "Додатково", {'fields': ('division_name', 'oklad', 'birthday', 'phone', 'adress', 'photo')}
        )
    )
    search_fields = ('tabel', 'fio')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50")

    get_html_photo.short_description = 'Мініатюра'


admin.site.register(Staff, StaffAdmin)


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('division_name', 'release_date', "doc_status", "doc_type", "doc_name", "display_author")
    list_filter = ('division_name', 'doc_status', 'doc_type')
    search_fields = ('doc_name',)
    prepopulated_fields = {'slug': ('doc_name',)}



@admin.register(Timesheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('date', "fio", "is_8", "is_7", "is_sick", 'is_vacation', 'is_unknown')
    list_filter = ('date', "fio", "is_8", "is_7", "is_sick", 'is_vacation', 'is_unknown')
    search_fields = ('fio',)
    list_editable = ("is_8", "is_7", "is_sick", 'is_vacation', 'is_unknown')
    prepopulated_fields = {'slug': ('date',)}


# Изменяет название страницы административной панели и название заголовка административной панали
admin.site.site_title = "Портал НДВ"
admin.site.site_header = "Портал НДВ"
