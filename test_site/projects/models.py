from django.db import models
from django.urls import reverse

# Create your models here.
from divisions.models import Divisions
from nio_app.models import Categories
from staff.models import Staff


class Projects(models.Model):
    """Проекти підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва проекту')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети проекту',
                                   verbose_name='Опис проекту')

    div = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Назва підрозділу', null=True)

    author = models.ManyToManyField(Staff, verbose_name='Автор', help_text="Оберіть автора/авторів проекту", )

    category = models.ManyToManyField(Categories, help_text='оберіть категорію/категорії',
                                      verbose_name='Оберіть категорію')

    docs = models.ManyToManyField('ProjectsDocs', verbose_name='Документ до проекту')

    pics = models.ManyToManyField('ProjectsPics', verbose_name='Картинка до проекту')

    objects = models.Manager()

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекти'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:project_single", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviewsprojects_set.filter(parent__isnull=True)


class ProjectsDocs(models.Model):
    """Файли проекту"""

    project = models.ForeignKey(Projects, on_delete=models.SET_NULL, verbose_name='Проект', null=True)

    """Шлях до файлів проекту"""

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/{instance.project.div.slug}/projects/{instance.project.pk}/{instance.project.slug}/{filename}'

    doc = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)

    objects = models.Manager()

    def file_load(self):
        self.doc.upload_to = f'archives/{self.project.div.slug}/projects/{self.project.pk}/'
        return self.doc.upload_to

    file_load.short_description = 'Розташування файлів'

    class Meta:
        verbose_name = 'Документ проекту'
        verbose_name_plural = 'Документи проектів'
        ordering = ['project']

    def __str__(self):
        return f'{self.doc}'


class ProjectsPics(models.Model):
    """Картинки проекту"""
    project = models.ForeignKey(Projects, on_delete=models.SET_NULL, verbose_name='Проект', null=True)

    """Шлях до картинок проекту"""

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/{instance.project.div.slug}/projects/{instance.project.pk}/{instance.project.slug}/{filename}'

    pic = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True,
                            max_length=500)

    objects = models.Manager()

    def file_load(self):
        self.pic.upload_to = f'archives/{self.project.div.slug}/projects/{self.project.pk}/'
        return self.pic.upload_to

    file_load.short_description = 'Розташування файлів'

    class Meta:
        verbose_name = 'Картинка проекту'
        verbose_name_plural = 'Картинки проектів'
        ordering = ['project']

    def __str__(self):
        return f'{self.pic}'


class ReviewsProjects(models.Model):
    """Відгуки на проект"""
    email = models.EmailField()
    name = models.CharField(verbose_name="Ім'я", max_length=100)
    text = models.TextField(verbose_name="Повідомлення", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="До кого", on_delete=models.SET_NULL, blank=True, null=True
    )
    project = models.ForeignKey(Projects, verbose_name="Проект", on_delete=models.CASCADE)

    pub_date = models.DateTimeField(verbose_name='Дата коментарія', null=True, auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} - {self.project}"

    class Meta:
        verbose_name = "Відгук на проект"
        verbose_name_plural = "Відгуки на проект"
        ordering = ['-pub_date']
