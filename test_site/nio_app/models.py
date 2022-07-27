from django.db import models
from django.urls import reverse
from django.contrib import admin


# Create your models here.

class Main(models.Model):
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва підрозділу')

    abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                           verbose_name='Абрівіатура підрозділу')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис підрозділу',
                                       verbose_name='Опис підрозділу')
    num_staff = models.IntegerField(verbose_name='Кількість персоналу', null=True)

    num_projects = models.IntegerField(verbose_name='Кількість проектів', null=True)

    num_docs = models.IntegerField(verbose_name='Кількість проектів', null=True)

    divisions = models.ManyToManyField('Divisions', verbose_name='Підрозділи', related_name=f'{slug}')

    boss = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='ПІБ керівника')

    photo = models.ImageField(upload_to="workers_foto/", verbose_name="Фото")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Загальна інфо'
        verbose_name_plural = 'Загальна інфо'

    def __str__(self):
        return self.abr


class Divisions(models.Model):
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                                     verbose_name='Назва підрозділу')

    abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                               verbose_name='Абрівіатура підрозділу')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис підрозділу',
                                       verbose_name='Опис підрозділу')

    num_staff = models.IntegerField(verbose_name='Кількість персоналу', null=True)

    num_projects = models.IntegerField(verbose_name='Кількість проектів', null=True)

    num_docs = models.IntegerField(verbose_name='Кількість проектів', null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Підрозділи'
        verbose_name_plural = 'Підрозділи'

    def __str__(self):
        return self.abr


class Staff(models.Model):
    fio = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                           verbose_name='ПІБ')

    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    div_name = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Назва підрозділу', null=True, related_name=f'{slug}')

    tabel = models.CharField(max_length=5, help_text='не більше ніж 5 символів', verbose_name='Табельный номер', unique=True)

    prof = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                            verbose_name='Професія')

    oklad = models.IntegerField(verbose_name='Оклад')

    birthday = models.DateField(verbose_name="Дата народження", blank=True)

    phone = models.CharField(max_length=18, help_text='формат +38(ХХХ)-ХХХ-ХХ-ХХ',
                             verbose_name='Номер телефону')

    adress = models.CharField(max_length=100, help_text='формат пр/вул/провулок ХХХХХ д.ХХ кв.ХХ',
                              verbose_name='Домашня адреса')

    photo = models.ImageField(upload_to="workers_foto/", verbose_name="Фото")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return self.fio



class Documents(models.Model):
    CHOICES_DOC_TYPE = (
        ("М", "Методика"), ("П", "Паспорт"), ("КЕ", "Керівництво з експлуатації"), ("ТД", "Технична довідка"),
        ("ЗТ", "Технічний звіт"), ("ТІ", "Технологічна інструкция"), ("І", "Інше"), (None, "Тип"))

    CHOICES_STATUS = (("Р", "Розробка"), ("У", "Узгодження"), ("В", "Впроваджено"), (None, "Статус"))

    name = models.CharField(max_length=500, help_text="Введіть назву документу",
                                verbose_name="Назва документа")

    slug = models.SlugField(max_length=500, unique=True, verbose_name='URL', db_index=True)

    div_name = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Назва підрозділу')

    author = models.ManyToManyField(Staff, verbose_name='Автор', help_text="Оберіть автора/авторів документу", related_name='authors')

    type = models.CharField(max_length=50, help_text="Оберіть тип документу",
                                verbose_name="Тип документу", choices=CHOICES_DOC_TYPE)

    status = models.CharField(max_length=50, help_text="Поточний статус документу",
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
        ordering = ['div_name']

    def __str__(self):
        return self.name