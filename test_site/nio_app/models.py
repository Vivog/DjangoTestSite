from django.db import models
from django.urls import reverse


# Create your models here.


class Divisions(models.Model):
    division_name = models.CharField(max_length=50, help_text='не більше ніж 50 символів',
                                     verbose_name='Назва підрозділу')

    def __str__(self):
        return self.division_name


class Staff(models.Model):
    fio = models.CharField(max_length=50, help_text='не більше ніж 30 символів',
                           verbose_name='ПІБ')
    division_name = models.ForeignKey("Divisions", on_delete=models.CASCADE, help_text='не більше ніж 50 символів',
                                      verbose_name='Назва підрозділу')
    tabel = models.IntegerField(verbose_name='Табельный номер')
    oklad = models.IntegerField(verbose_name='Оклад')
    birthday = models.DateField(verbose_name="Дата народження", blank=True, null=True)

    def __str__(self):
        return f"{self.fio}"

    def get_absolute_url(self):
        return reverse('stuff-detail', args=[str(self.id)])


class Condition(models.Model):
    CHOICES_COND = (
        ("8", "Повний день 8"), ("7", "Повний день 7"), ("Б", "Лікарняний"), ("О", "Відпустка"),
        ("Н", "Невідома причина"))
    cond_status = models.CharField(max_length=5, help_text="Оберіть один з варіантів",
                                   verbose_name="Свідчення присутності", choices=CHOICES_COND)

    def __str__(self):
        return self.cond_status


class Timesheet(models.Model):
    fio = models.ForeignKey('Staff', on_delete=models.CASCADE, verbose_name='ПІБ', related_name='timesheet_fio')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, verbose_name="Свідчення присутності")
    date = models.DateField(help_text='Оберіть дату', verbose_name='Дата табелювання')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.condition} | {self.date} | {self.fio}"


class Documents(models.Model):
    doc_name = models.CharField(max_length=200, help_text="Введіть назву документу",
                                verbose_name="Назва документа")
    author = models.ManyToManyField("Staff", verbose_name='ПІБ',
                                    help_text="Введіть автора документу")

    CHOICES_DOC_TYPE = (
        ("М", "Методика"), ("П", "Паспорт"), ("КЭ", "Керівництво з експлуатації"), ("ТД", "Технична довідка"),
        ("ЗТ", "Техничний звіт"), ("ТІ", "Технологічна інструкция"), ("І", "Інше"),)
    doc_type = models.CharField(max_length=50, help_text="Введіть тип документу",
                                verbose_name="Тип документу", choices=CHOICES_DOC_TYPE)

    CHOICES_STATUS = (("Р", "Розробка"), ("С", "Узгодження"), ("В", "Впроваджено"))
    doc_status = models.CharField(max_length=50, help_text="Поточний статус документу",
                                  verbose_name="Статус документу", choices=CHOICES_STATUS)
    release_date = models.DateField(help_text="Введіть дату впровадження", verbose_name="Дата впровадження",
                                    blank=True, null=True)

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'

    def __str__(self):
        return f"{self.release_date} | {self.doc_status} |{self.doc_type} | {self.doc_name} | {self.author}"
