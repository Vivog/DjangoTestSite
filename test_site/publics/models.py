from django.db import models
from django.urls import reverse
from staff.models import Staff
from divisions.models import Divisions
from nio_app.models import Categories

# Create your models here.
class Publications(models.Model):
    """Публікації підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва публікації')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети публікації',
                                   verbose_name='Короткий опис', null=True)

    text = models.TextField(max_length=50000, help_text='не більше 50 000 символів',
                            verbose_name='Текст публікації', null=True)

    div = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Назва підрозділу', null=True)

    author = models.ManyToManyField(Staff, verbose_name='Автор', help_text="Оберіть автора/авторів публікації", )

    category = models.ManyToManyField(Categories, help_text='оберіть категорію/категорії',
                                      verbose_name='Оберіть категорію')

    pub_date = models.DateField(verbose_name='Дата піблікації', null=True)

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/{instance.div.slug}/publications/{instance.pub_date}/{instance.slug}/{filename}'

    photo_1 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", null=True, max_length=500)
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True,
                                max_length=500)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True,
                                max_length=500)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True,
                                max_length=500)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True,
                                max_length=500)

    doc = models.FileField(upload_to=directory_path, blank=True, null=True, verbose_name='Файл публікації',
                           max_length=500)

    objects = models.Manager()

    def file_load(self):
        self.doc.upload_to = f'archives/{self.div.slug}/publications/{self.pub_date}/{self.slug}/'
        return self.doc.upload_to

    file_load.short_description = 'Розташування файлів'

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'

    class Meta:
        verbose_name = 'Публікація'
        verbose_name_plural = 'Публікації'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nio_app:public_single", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviewspubs_set.filter(parent__isnull=True)


class ReviewsPubs(models.Model):
    """Відгуки на публікацію"""
    email = models.EmailField()
    name = models.CharField(verbose_name="Ім'я", max_length=100)
    text = models.TextField(verbose_name="Повідомлення", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="До кого", on_delete=models.SET_NULL, blank=True, null=True
    )
    pub = models.ForeignKey(Publications, verbose_name="Публікація", on_delete=models.CASCADE)

    pub_date = models.DateTimeField(verbose_name='Дата коментарія', null=True, auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - {self.pub}"

    class Meta:
        verbose_name = "Відгук на публікацію"
        verbose_name_plural = "Відгуки на публікацію"
        ordering = ['-pub_date']
