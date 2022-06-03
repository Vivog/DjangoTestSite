from django.db import models
from django.urls import reverse


# Create your models here.


class Divisions(models.Model):
    division_name = models.CharField(max_length=50, help_text='не более 50 символов',
                                     verbose_name='Название подразделение')

    def __str__(self):
        return self.division_name


class Staff(models.Model):
    fio = models.CharField(max_length=30, help_text='не более 30 символов',
                           verbose_name='ФИО')
    division_name = models.ForeignKey("Divisions", on_delete=models.CASCADE, help_text='не более 50 символов',
                                      verbose_name='Название подразделение')
    tabel = models.IntegerField(verbose_name='Табельный номер')
    oklad = models.IntegerField(verbose_name='Оклад')
    birthday = models.DateField(verbose_name="Дата рождения", blank=True, null=True)

    def __str__(self):
        return f"{self.tabel} | {self.fio} | {self.division_name}"

    def get_absolute_url(self):
        return reverse('stuff-detail', args=[str(self.id)])


class Condition(models.Model):
    CHOICES_COND = (
        ("8", "Полный день"), ("7", "Полный день"), ("Б", "Больничный"), ("О", "Отпуск"), ("Н", "Неизвестная причина"))
    cond_status = models.CharField(max_length=5, help_text="Выберите один из вариантов",
                                   verbose_name="Сведения присутствия", choices=CHOICES_COND)

    def __str__(self):
        return self.cond_status


class Timesheet(models.Model):
    fio = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name='ФИО', related_name='timesheet_fio')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, verbose_name="Сведения присутствия")
    date = models.DateField(help_text='Выберите дату', verbose_name='Дата табелирования')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.condition} | {self.date} | {self.fio}"


class Documents(models.Model):
    doc_name = models.CharField(max_length=200, help_text="Введите название документа",
                                verbose_name="Название документа")
    author = models.ManyToManyField('Staff', verbose_name='ФИО',
                                    help_text="Введите автора документа")

    CHOICES_DOC_TYPE = (
        ("М", "Методика"), ("П", "Паспорт"), ("РЭ", "Руководство по эксплуатации"), ("ТС", "Техническая справка"),
        ("ОТ", "Технический отчет"), ("ТИ", "Технологическая инструкция"), ("Д", "Другое"),)
    doc_type = models.CharField(max_length=50, help_text="Введите тип документа",
                                verbose_name="Тип документа", choices=CHOICES_DOC_TYPE)

    CHOICES_STATUS = (("Р", "Разработка"), ("С", "Согласование"), ("В", "Внедрено"))
    doc_status = models.CharField(max_length=50, help_text="Текущий статус документа",
                                  verbose_name="Статус документа", choices=CHOICES_STATUS)
    release_date = models.DateField(help_text="Введите дату внедрения", verbose_name="Дата внедрения",
                                    blank=True, null=True)

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'

    def __str__(self):
        return f"{self.release_date} | {self.doc_status} |{self.doc_type} | {self.doc_name} | {self.author}"
