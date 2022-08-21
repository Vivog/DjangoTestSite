from django.db import models
from django.urls import reverse

# Create your models here.

class Main(models.Model):
    """Головна модель загального підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва підрозділу')

    abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                           verbose_name='Абрівіатура підрозділу')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    divisions = models.ManyToManyField('Divisions', verbose_name='Підрозділи')

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


class Divisions(models.Model):
    """Підрозіл що входить до загального підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва підрозділу')

    abr = models.CharField(max_length=10, help_text='не більше ніж 10 символів',
                           verbose_name='Абрівіатура підрозділу')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис підрозділу',
                                   verbose_name='Опис підрозділу')

    num_staff = models.IntegerField(verbose_name='Кількість персоналу', null=True, blank=True, default=0)

    num_projects = models.IntegerField(verbose_name='Кількість проектів', null=True)

    num_docs = models.IntegerField(verbose_name='Загальна кількість документації', null=True)

    locs = models.ManyToManyField('Location', verbose_name='Розміщення')

    coops = models.ManyToManyField('Cooperation', verbose_name='Підрозділи взаємодії')

    theses = models.ManyToManyField('Theses', verbose_name='Тези')

    boss = models.CharField(max_length=50, help_text='Призвище Ім\'я',
                            verbose_name='ПІБ керівника', null=True, blank=True)

    photo = models.ImageField(upload_to="boss_foto/", verbose_name="Фото")

    """Шлях до фото підрозділу"""
    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'divs/{instance.slug}/photo/{filename}'

    photo_1 = models.ImageField(upload_to=directory_path, verbose_name="Фото підрозділу", null=True)
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Фото підрозділу", blank=True, null=True)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Фото підрозділу", blank=True, null=True)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Фото підрозділу", blank=True, null=True)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Фото підрозділу", blank=True, null=True)

    objects = models.Manager()

    __original_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

    """Визначення кількості персоналу, проектів та документації через сумісні моделі"""
    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()
        self.num_staff = len(Staff.objects.filter(div_id=self.pk))
        self.num_projects = len(Projects.objects.filter(div_id=self.pk))
        self.num_docs = len(Documents.objects.filter(div_id=self.pk))
        super().save(force_insert=False, force_update=True, using=using, update_fields=update_fields)

    class Meta:
        verbose_name = 'Підрозділи'
        verbose_name_plural = 'Підрозділи'
        ordering = ['name']

    def __str__(self):
        return self.abr


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

    staff = Staff.objects.filter(fio__icontains='Віталій')

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


class Projects(models.Model):
    """Проекти підрозділу"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва проекту')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети проекту',
                                   verbose_name='Опис підрозділу')

    div = models.ForeignKey(Divisions, on_delete=models.SET_NULL, verbose_name='Назва підрозділу', null=True)

    author = models.ManyToManyField(Staff, verbose_name='Автор', help_text="Оберіть автора/авторів проекту", )

    category = models.ManyToManyField('Categories', help_text='оберіть категорію/категорії',
                                      verbose_name='Оберіть категорію')

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/{instance.div.slug}/projects/{instance.pk}/{instance.slug}/{filename}'

    doc_1 = models.FileField(upload_to=directory_path, null=True, max_length=500)
    doc_2 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_3 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_4 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_5 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_6 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_7 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_8 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_9 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)
    doc_10 = models.FileField(upload_to=directory_path, blank=True, null=True, max_length=500)

    photo_1 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", null=True, max_length=500)
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True,
                                max_length=500)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True,
                                max_length=500)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True,
                                max_length=500)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True,
                                max_length=500)

    objects = models.Manager()

    def file_load(self):
        self.doc.upload_to = f'archives/{self.div.slug}/projects/{self.pk}/'
        return self.doc.upload_to

    file_load.short_description = 'Розташування файлів'

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекти'
        ordering = ['name']

    def __str__(self):
        return self.name


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

    category = models.ManyToManyField('Categories', help_text='оберіть категорію/категорії',
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


class News(models.Model):
    """Загальні новини"""
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва новини')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети новини',
                                   verbose_name='Короткий опис', null=True)

    text = models.TextField(max_length=15000, help_text='не більше 15 000 символів',
                            verbose_name='Текст новини', null=True)

    category = models.ManyToManyField('Categories', help_text='оберіть категорію/категорії',
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
