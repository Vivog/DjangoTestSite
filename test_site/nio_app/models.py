from django.db import models
from django.urls import reverse
from django.contrib import admin


# Create your models here.


class Divisions(models.Model):

    division_name = models.CharField(max_length=50, help_text='не більше ніж 50 символів',
                                     verbose_name='Назва підрозділу')
    div_abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                               verbose_name='Абрівіатура підрозділу')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    div_description = models.TextField(max_length=1000, help_text='Введіть короткий опис підрозділу',
                                       verbose_name='Опис підрозділу')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Підрозділи'
        verbose_name_plural = 'Підрозділи'

    def __str__(self):
        return self.division_name

    def get_absolute_url(self):
        return reverse('division-detail', kwargs={'div_slug': self.slug})



class Staff(models.Model):

    fio = models.CharField(max_length=50, help_text='не більше ніж 30 символів',
                           verbose_name='ПІБ')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)
    division_name = models.ForeignKey("Divisions", on_delete=models.CASCADE, help_text='не більше ніж 50 символів',
                                      verbose_name='Назва підрозділу', null=True)
    tabel = models.IntegerField(verbose_name='Табельный номер', unique=True)
    prof = models.CharField(max_length=50, help_text='не більше ніж 30 символів',
                           verbose_name='Професія')
    oklad = models.IntegerField(verbose_name='Оклад')
    birthday = models.DateField(verbose_name="Дата народження", blank=True)
    phone = models.CharField(max_length=18, help_text='формат +38(ХХХ)-ХХХ-ХХ-ХХ',
                           verbose_name='Номер телефону')
    adress = models.CharField(max_length=50, help_text='формат пр/вул/провулок ХХХХХ д.ХХ кв.ХХ',
                           verbose_name='Домашня адреса')
    photo = models.ImageField(upload_to="workers_foto/", verbose_name="Фото")
    objects = models.Manager()

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return f"{self.fio}"

    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'staff_slug': self.slug})


class Timesheet(models.Model):

    fio = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name='ПІБ', related_name='timesheet_fio')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)
    date = models.DateField(help_text='Оберіть дату', verbose_name='Дата табелювання')
    is_8 = models.BooleanField(verbose_name='8',  default=True)
    is_7 = models.BooleanField(verbose_name='7',  default=False)
    is_sick = models.BooleanField(verbose_name='Л', default=False)
    is_vacation = models.BooleanField(verbose_name='В',  default=False)
    is_unknown = models.BooleanField(verbose_name='Н',  default=False)

    class Meta:
        ordering = ['date']
        verbose_name = 'Табельний облік'
        verbose_name_plural = 'Табельний облік'

    def __str__(self):
        return f"{self.date} | {self.fio}"

    def get_absolute_url(self):
        return reverse('timesheet-detail', kwargs={'timesheet_slug': self.slug})


class Documents(models.Model):

    doc_name = models.CharField(max_length=200, help_text="Введіть назву документу",
                                verbose_name="Назва документа")
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    division_name = models.ForeignKey("Divisions", on_delete=models.CASCADE, help_text='не більше ніж 50 символів',
                                      verbose_name='Назва підрозділу')

    author = models.ManyToManyField("Staff", verbose_name='Автор',
                                    help_text="Введіть автора документу", related_name='authors')




    CHOICES_DOC_TYPE = (
        ("М", "Методика"), ("П", "Паспорт"), ("КЕ", "Керівництво з експлуатації"), ("ТД", "Технична довідка"),
        ("ЗТ", "Технічний звіт"), ("ТІ", "Технологічна інструкция"), ("І", "Інше"),)
    doc_type = models.CharField(max_length=50, help_text="Введіть тип документу",
                                verbose_name="Тип документу", choices=CHOICES_DOC_TYPE)

    CHOICES_STATUS = (("Р", "Розробка"), ("У", "Узгодження"), ("В", "Впроваджено"))
    doc_status = models.CharField(max_length=50, help_text="Поточний статус документу",
                                  verbose_name="Статус документу", choices=CHOICES_STATUS)
    release_date = models.DateField(help_text="Введіть дату впровадження", verbose_name="Дата впровадження",
                                    blank=True, null=True)
    objects = models.Manager()

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'


    class Meta:
        verbose_name = 'Документація'
        verbose_name_plural = 'Документація'
        ordering = ['division_name']

    def __str__(self):
        return f"{self.division_name}"

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'doc_slug': self.slug})
