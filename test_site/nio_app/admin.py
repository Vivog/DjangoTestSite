from django.contrib import admin

from .models import Divisions, Staff, Condition, Documents, Timesheet

# Register your models here.

admin.site.register(Divisions)
# admin.site.register(Staff)
admin.site.register(Condition)
# admin.site.register(Documents)
admin.site.register(Timesheet)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('tabel', 'fio', 'division_name')


admin.site.register(Staff, StaffAdmin)


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('release_date', "doc_status", "doc_type", "doc_name", "display_author")
