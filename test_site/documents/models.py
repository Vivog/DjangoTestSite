from django.db import models

# Create your models here.
from staff.models import Staff
from divisions.models import Divisions


class Documents(models.Model):
    """Документація підрозділу"""
    CHOICES_DOC_TYPE = (
        ("M", "Методики"), ("P", "Паспорти"), ("KE", "Керівництва з експлуатації"), ("TD", "Техничні довідки"),
        ("ZT", "Технічні звіти"), ("TI", "Технологічні інструкції"), ("I", "Інше"), (None, "Тип"))

    CHOICES_STATUS = (("Р", "Розробка"), ("У", "Узгодження"), ("В", "Впроваджено"), (None, "Статус"))

    year = models.CharField(max_length=4, help_text="Введіть рік випуску",
                            verbose_name="Рік випуску", null=True)

    number = models.CharField(max_length=20, help_text="Введіть номер документу",
                              verbose_name="Номер документа", null=True)

    name = models.CharField(max_length=500, help_text="Введіть назву документу",
                            verbose_name="Назва документа")

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис документа (мета)',
                                   verbose_name='Опис документа', null=True)

    slug = models.SlugField(max_length=500, unique=True, verbose_name='URL', db_index=True)

    div = models.ForeignKey(Divisions, on_delete=models.SET_NULL, null=True, verbose_name='Назва підрозділу',
                            related_name='div')

    author = models.ManyToManyField(Staff, verbose_name='Автор', help_text="Оберіть автора/авторів документу",
                                    related_name='authors')

    type = models.CharField(max_length=50, help_text="Оберіть тип документу",
                            verbose_name="Тип документу", choices=CHOICES_DOC_TYPE)

    status = models.CharField(max_length=50, help_text="Поточний статус документу",
                              verbose_name="Статус документу", choices=CHOICES_STATUS)

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/{instance.div.slug}/{instance.type}/{filename}'

    doc = models.FileField(upload_to=directory_path)

    release_date = models.DateField(help_text="Введіть дату впровадження", verbose_name="Дата впровадження",
                                    blank=True, null=True)
    objects = models.Manager()

    # staff = Staff.objects.filter(fio__icontains='Віталій')

    def display_author(self):
        return ', '.join([self.staff.fio.split()[0] for self.staff in self.author.all()])

    display_author.short_description = 'Автори'

    def file_load(self):
        self.doc.upload_to = f'archives/{self.div.slug}/{self.type}/'
        return self.doc.upload_to

    file_load.short_description = 'Розташування файлу'

    class Meta:
        verbose_name = 'Документація'
        verbose_name_plural = 'Документація'
        ordering = ['-release_date']

    def __str__(self):
        return f'{self.year}_{self.number}_{self.name}'
