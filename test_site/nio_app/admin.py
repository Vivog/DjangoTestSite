from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Divisions)
# # admin.site.register(Staff)
# admin.site.register(Condition)
# admin.site.register(Documents)
# admin.site.register(Timesheet)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('tabel', 'fio', 'division_name')
    list_display_links = ('tabel', 'fio')
    list_filter = ('division_name',)
    # Разбиение подробной информации на секции
    # сначало название секции, потом поля для отображения
    # если название не нужно то пишим None
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('tabel', 'fio')}
        ),
        (
            "Додатково", {'fields': ('division_name', 'oklad', 'birthday')}
        )
    )
    search_fields = ('tabel', 'fio')

admin.site.register(Staff, StaffAdmin)


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('release_date', "doc_status", "doc_type", "doc_name", "display_author")
    list_filter = ('doc_status', 'doc_type')
    search_fields = ('doc_name',)
    # можно также поменять расположение полей выводимой информации
    # fields = ["doc_status", "doc_type", 'release_date'] это будет вывод полей по вертикали
    # если нужно довыести что то по горизонтали, то внутри этого же списка объединяем в кортеж те поля
    # которые необходимо выводить по горизонтали
    # fields = ['release_date', ('doc_status', 'doc_type')]
    # чтобы исключить какие-то поля из отображения, применяем
    # exclude = ['doc_name']

@admin.register(Timesheet)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('date', "fio", "is_8", "is_7", "is_sick", 'is_vacation', 'is_unknown')
    list_filter = ('date', "fio", "is_8", "is_7", "is_sick", 'is_vacation', 'is_unknown')
    search_fields = ('fio',)