from django.db import models

# Create your models here.


class Main(models.Model):
    """Головна модель загального підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва підрозділу')

    abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                           verbose_name='Абрівіатура підрозділу')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис підрозділу',
                                   verbose_name='Опис підрозділу')

    num_staff = models.IntegerField(verbose_name='Кількість персоналу', null=True, blank=True)

    num_projects = models.IntegerField(verbose_name='Кількість проектів', null=True, blank=True)

    num_docs = models.IntegerField(verbose_name='Загальна кількість документації', null=True, blank=True)

    boss = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='ПІБ керівника')

    photo = models.ImageField(upload_to="workers_foto/", verbose_name="Фото")

    objects = models.Manager()

    """Визначення загальної кількості персоналу"""

    def staff(self):
        num = 0
        for d in self.divisions.all():
            if d.num_staff:
                num += d.num_staff
                self.num_staff = num
            else:
                self.num_staff = 0
        return self.num_staff

    staff.short_description = 'Загальна кількість персоналу'

    class Meta:
        verbose_name = 'Загальна інфо'
        verbose_name_plural = 'Загальна інфо'

    def __str__(self):
        return self.abr


class Location(models.Model):
    """Приміщення підрозділу"""
    loc = models.CharField(max_length=100, help_text='Вкажіть приміщення або цех(приміщення)',
                           verbose_name='Приміщення')

    object = models.Manager()

    def __str__(self):
        return self.loc

    class Meta:
        verbose_name = 'Приміщення'
        verbose_name_plural = 'Приміщення'
        ordering = ['loc']


class Cooperation(models.Model):
    """Сумісні підрозділи"""
    name = models.CharField(max_length=100, help_text='Вкажіть пов\'язаний підрозділ',
                            verbose_name='Підрозділ')

    object = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Підрозділ взаємодії'
        verbose_name_plural = 'Підрозділи взаємодії'
        ordering = ['name']



class Theses(models.Model):
    """Тезіси що характеризують підрозділ"""
    name = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                            verbose_name='Теза')

    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    photo = models.ImageField(upload_to="theses/", verbose_name="Картинка")

    objects = models.Manager()

    class Meta:
        verbose_name = 'Теза'
        verbose_name_plural = 'Тези'

    def __str__(self):
        return self.name


class Categories(models.Model):
    """Категорії до публікацій та новин"""
    name = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                            verbose_name='Категорія')

    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name
