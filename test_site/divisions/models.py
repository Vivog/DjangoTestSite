from django.db import models
from nio_app.models import Location, Cooperation, Theses

# Create your models here.


class Divisions(models.Model):
    """Підрозіл що входить до загального підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва підрозділу')

    abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                           verbose_name='Абрівіатура підрозділу')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    main_div = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                           verbose_name='Абрівіатура підрозділу', null=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис підрозділу',
                                   verbose_name='Опис підрозділу')

    locs = models.ManyToManyField(Location, verbose_name='Розміщення')

    coops = models.ManyToManyField(Cooperation, verbose_name='Підрозділи взаємодії')

    theses = models.ManyToManyField(Theses, verbose_name='Тези')

    pics = models.ManyToManyField('DivisionsPics', verbose_name='Картинка до підрозділу')

    """Шлях до фото підрозділу"""

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'divs/{instance.slug}/photo/{filename}'

    objects = models.Manager()

    __original_name = None

    class Meta:
        verbose_name = 'Підрозділи'
        verbose_name_plural = 'Підрозділи'
        ordering = ['name']

    def __str__(self):
        return self.abr


class DivisionsPics(models.Model):
    """Картинки що відображають діяльність підрозділів"""

    # div = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Підрозділ', null=True)

    """Шлях до фото підрозділу"""

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'divs/{instance.div.slug}/photo/{filename}'

    pic = models.ImageField(upload_to=directory_path, verbose_name="Фото підрозділу", blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Картинка до підрозділу'
        verbose_name_plural = 'Картинки до підрозділів'

    def __str__(self):
        return f'{self.pic}'
