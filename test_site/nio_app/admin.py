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


@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ('abr', 'boss', 'num_staff', 'get_html_photo')
    prepopulated_fields = {'slug': ('abr',)}
    readonly_fields = ('get_html_photo', )
    fieldsets = (
        (
            "Загальні відомості", {'fields': ('name', ('abr', 'slug'), 'description')}
        ),
        (
            "Додатково", {'fields': (('num_staff', 'num_docs', 'num_projects'), ('locs', 'coops', 'theses',) )}
        ),
        (
            'Управління', {'fields': ('boss', 'photo', 'get_html_photo')}
        ),
        (
            'Додаткові фото', {'fields': ('photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5')}
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['num_staff'].initial = 0
        form.base_fields['num_projects'].initial = 0
        form.base_fields['num_docs'].initial = 0
        return form

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100")

    get_html_photo.short_description = 'Мініатюра'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('div', 'tabel', 'fio', 'get_html_photo',)
    prepopulated_fields = {'slug': ('fio',)}
    list_display_links = ('fio',)
    readonly_fields = ('get_html_photo', )
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

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100")

    get_html_photo.short_description = 'Мініатюра'


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('div', 'release_date', "status", "type", "name", "display_author", 'file_load')
    list_display_links = ('name',)
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
    list_display_links = ('name',)
    list_filter = ('div',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


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
    save_on_top = True
    inlines = [ReviewPubsInline]

@admin.register(ReviewsPubs)
class ReviewPubsAdmin(admin.ModelAdmin):
    """Відгуки до публікації"""
    list_display = ("name", "email", "parent", "pub")
    readonly_fields = ("name", "email")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # fields = ('fio')
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True

@admin.register(ReviewsNews)
class ReviewNewsAdmin(admin.ModelAdmin):
    """Відгуки до новини"""
    list_display = ("name", "email", "parent", "news")
    readonly_fields = ("name", "email")

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
