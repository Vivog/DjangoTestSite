from django.db import models
from django.shortcuts import reverse

# Create your models here.
from nio_app.models import Categories


class News(models.Model):
    """Загальні новини"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва новини')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети новини',
                                   verbose_name='Короткий опис', null=True)

    text = models.TextField(max_length=15000, help_text='не більше 15 000 символів',
                            verbose_name='Текст новини', null=True)

    category = models.ManyToManyField(Categories, help_text='оберіть категорію/категорії',
                                      verbose_name='Оберіть категорію')

    pub_date = models.DateField(verbose_name='Дата новини', null=True)

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/news/{instance.pub_date}/{instance.slug}/{filename}'

    photo_1 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", null=True, max_length=500)
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True,
                                max_length=500)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True,
                                max_length=500)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True,
                                max_length=500)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True,
                                max_length=500)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nio_app:news_single", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviewsnews_set.filter(parent__isnull=True)


class ReviewsNews(models.Model):
    """Відгуки на новину"""
    email = models.EmailField()
    name = models.CharField(verbose_name="Ім'я", max_length=100)
    text = models.TextField(verbose_name="Повідомлення", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="До кого", on_delete=models.SET_NULL, blank=True, null=True
    )
    news = models.ForeignKey(News, verbose_name="Новина", on_delete=models.CASCADE)

    pub_date = models.DateTimeField(verbose_name='Дата коментарія', null=True, auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - {self.news}"

    class Meta:
        verbose_name = "Відгук на новину"
        verbose_name_plural = "Відгуки на новину"
        ordering = ['-pub_date']