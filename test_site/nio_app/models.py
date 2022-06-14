from django.db import models
from django.urls import reverse


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
                                      verbose_name='Назва підрозділу')
    tabel = models.IntegerField(verbose_name='Табельный номер')
    oklad = models.IntegerField(verbose_name='Оклад')
    birthday = models.DateField(verbose_name="Дата народження", blank=True, null=True)
    photo = models.ImageField(upload_to="workers_foto/", verbose_name="Фото", null=True)
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
                                      verbose_name='Назва підрозділу', null=True)

    author = models.ManyToManyField("Staff", verbose_name='ПІБ',
                                    help_text="Введіть автора документу")

    CHOICES_DOC_TYPE = (
        ("М", "Методика"), ("П", "Паспорт"), ("КЕ", "Керівництво з експлуатації"), ("ТД", "Технична довідка"),
        ("ЗТ", "Техничний звіт"), ("ТІ", "Технологічна інструкция"), ("І", "Інше"),)
    doc_type = models.CharField(max_length=50, help_text="Введіть тип документу",
                                verbose_name="Тип документу", choices=CHOICES_DOC_TYPE)

    CHOICES_STATUS = (("Р", "Розробка"), ("С", "Узгодження"), ("В", "Впроваджено"))
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

    def __str__(self):
        return self.doc_name

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'doc_slug': self.slug})
