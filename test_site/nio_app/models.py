from django.db import models
from django.urls import reverse


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=30, help_text='не более 30 символов',
                                       verbose_name='Название отдела')
    fio_chief = models.ManyToManyField('Staff', verbose_name='ФИО')
    tabel = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name='Табельный номер')

    def __str__(self):
        return self.department_name


class Divisions(models.Model):
    division_name = models.CharField(max_length=50, help_text='не более 50 символов',
                                     verbose_name='Название подразделение')
    fio_chief = models.ManyToManyField('Staff', verbose_name='ФИО')
    tabel = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name='Табельный номер')

    def __str__(self):
        return self.division_name


class Staff(models.Model):
    fio = models.CharField(max_length=30, help_text='не более 30 символов',
                           verbose_name='ФИО')
    division_name = models.ManyToManyField(Divisions, help_text='не более 50 символов',
                                           verbose_name='Название подразделение')
    tabel = models.IntegerField(verbose_name='Табельный номер')
    oklad = models.IntegerField(verbose_name='Оклад')
    birthday = models.DateField(verbose_name="Дата рождения", blank=True, null=True)

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('stuff-detail', args=[str(self.id)])


class Documents(models.Model):
    doc_name = models.CharField(max_length=200, help_text="Введите название документа",
                                verbose_name="Название документа")
    author = models.ManyToManyField('Staff', verbose_name='ФИО', help_text="Введите автора документа")

    CHOICES_DOC_TYPE = ["Методика", "Паспорт", "Руководство по эксплуатации", "Техническая справка",
                        "Технический отчет", "Технологическая инструкция", "Другое"]
    doc_type = models.CharField(max_length=50, help_text="Введите тип документа",
                                verbose_name="Название документа", choices=CHOICES_DOC_TYPE)

    CHOICES_STATUS = ["Разработка", "Согласование", "Внедрено"]
    doc_status = models.CharField(max_length=50, help_text="Текущий статус документа",
                                  verbose_name="Статус документа", choices=CHOICES_STATUS)

    release_date = models.DateField(help_text="Введите дату внедрения", verbose_name="Дата внедрения",
                                    blank=True, null=True)

    def __str__(self):
        return self.doc_name

    def get_absolute_url(self):
        return reverse('doc-detail', args=[str(self.id)])
