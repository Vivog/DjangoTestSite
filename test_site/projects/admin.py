from django.contrib import admin

# Register your models here.
from .models import Projects, ProjectsDocs, ProjectsPics


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'div', "display_author",)
    list_display_links = ('name',)
    list_filter = ('div',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectsPics)
class ProjectsPicsAdmin(admin.ModelAdmin):
    list_display = ('project', 'pic', 'file_load')


@admin.register(ProjectsDocs)
class ProjectsDocsAdmin(admin.ModelAdmin):
    list_display = ('project', 'doc', 'file_load')