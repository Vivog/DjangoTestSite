from django.db import models
from divisions.models import Divisions


# Create your models here.
class Staff(models.Model):
    """Персонал підрозділу"""
    fio = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                           verbose_name='ПІБ')

    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    div = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Підрозділ', null=True)

    tabel = models.CharField(max_length=5, help_text='не більше ніж 5 символів', verbose_name='Табельный номер',
                             unique=True)

    prof = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                            verbose_name='Посада')

    oklad = models.IntegerField(verbose_name='Оклад')

    birthday = models.DateField(verbose_name="Дата народження", blank=True)

    phone = models.CharField(max_length=18, help_text='формат +38(ХХХ)-ХХХ-ХХ-ХХ',
                             verbose_name='Номер телефону')

    adress = models.CharField(max_length=100, help_text='формат пр/вул/провулок ХХХХХ д.ХХ кв.ХХ',
                              verbose_name='Домашня адреса')

    photo = models.ImageField(upload_to="workers_foto/", verbose_name="Фото")

    objects = models.Manager()

    def save(
            self, force_insert=True, force_update=False, using=None, update_fields=None
    ):
        super().save()

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'
        ordering = ['fio']

    def __str__(self):
        return self.fio
