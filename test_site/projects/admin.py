from .models import Projects, ProjectsDocs, ProjectsPics
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.forms.widgets import *
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.
class ProjectsAdminForm(forms.ModelForm):
    description = forms.CharField(label='Опис документу', widget=CKEditorUploadingWidget())

    class Meta:
        model = Projects
        fields = '__all__'

class ReviewProjectsInline(admin.TabularInline):
    model = ReviewsProjects
    extra = 1
    readonly_fields = ('name', 'email')

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'div', "display_author",)
    list_display_links = ('name',)
    list_filter = ('div',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    form = ProjectsAdminForm
    save_on_top = True
    inlines = [ReviewProjectsInline]
    list_select_related = True


@admin.register(ProjectsPics)
class ProjectsPicsAdmin(admin.ModelAdmin):
    list_display = ('project', 'get_html_pic', 'file_load')
    def get_html_pic(self, object):
        if object.pic:
            return mark_safe(f"<img src='{object.pic.url}' width=100")

    get_html_pic.short_description = 'Мініатюра'


@admin.register(ProjectsDocs)
class ProjectsDocsAdmin(admin.ModelAdmin):
    list_display = ('project', 'doc', 'file_load')


@admin.register(ReviewsProjects)
class ReviewProjectsAdmin(admin.ModelAdmin):
    """Відгуки до публікації"""
    list_display = ("name", "email", "parent", "project")
    readonly_fields = ("name", "email")