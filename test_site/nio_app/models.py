from django.db import models


# Create your models here.

class Main(models.Model):
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

    boss = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='ПІБ керівника', null=True, blank=True)

    photo_boss = models.ImageField(upload_to="boss_foto/", verbose_name="Фото")

    photo_1 = models.ImageField(upload_to="theses/", verbose_name="Фото підрозділу", null=True)
    photo_2 = models.ImageField(upload_to="theses/", verbose_name="Фото підрозділу", blank=True, null=True)
    photo_3 = models.ImageField(upload_to="theses/", verbose_name="Фото підрозділу", blank=True, null=True)
    photo_4 = models.ImageField(upload_to="theses/", verbose_name="Фото підрозділу", blank=True, null=True)
    photo_5 = models.ImageField(upload_to="theses/", verbose_name="Фото підрозділу", blank=True, null=True)

    objects = models.Manager()

    __original_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

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

    def __str__(self):
        return self.fio


class Documents(models.Model):
    CHOICES_DOC_TYPE = (
        ("М", "Методика"), ("П", "Паспорт"), ("КЕ", "Керівництво з експлуатації"), ("ТД", "Технична довідка"),
        ("ЗТ", "Технічний звіт"), ("ТІ", "Технологічна інструкція"), ("І", "Інше"), (None, "Тип"))

    CHOICES_STATUS = (("Р", "Розробка"), ("У", "Узгодження"), ("В", "Впроваджено"), (None, "Статус"))

    name = models.CharField(max_length=500, help_text="Введіть назву документу",
                            verbose_name="Назва документа")

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

    def display_author(self):
        return ', '.join([staff.fio.split()[0] for staff in self.author.all()])

    display_author.short_description = 'Автори'

    def file_load(self):
        self.doc.upload_to = f'archives/{self.div.slug}/{self.type}/'
        return self.doc.upload_to

    file_load.short_description = 'Розташування файлу'

    class Meta:
        verbose_name = 'Документація'
        verbose_name_plural = 'Документація'
        ordering = ['div']

    def __str__(self):
        return self.name


class Location(models.Model):
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
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True, max_length=500)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True, max_length=500)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True, max_length=500)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Картинка проекту", blank=True, null=True, max_length=500)


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
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва публікації')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети публікації',
                                   verbose_name='Короткий опис', null=True)

    text = models.TextField(max_length=50000, help_text='Введіть короткий опис мети публікації',
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
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True, max_length=500)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True, max_length=500)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True, max_length=500)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Картинка публікації", blank=True, null=True, max_length=500)


    doc = models.FileField(upload_to=directory_path, blank=True, null=True, verbose_name='Файл публікації', max_length=500)

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
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=200, help_text='не більше ніж 200 символів',
                            verbose_name='Назва новини')

    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL', db_index=True)

    description = models.TextField(max_length=5000, help_text='Введіть короткий опис мети публікації',
                                   verbose_name='Короткий опис', null=True)

    text = models.TextField(max_length=15000, help_text='Введіть короткий опис мети публікації',
                                   verbose_name='Текст новини', null=True)

    category = models.ManyToManyField('Categories', help_text='оберіть категорію/категорії',
                            verbose_name='Оберіть категорію')

    pub_date = models.DateField(verbose_name='Дата піблікації', null=True)

    def directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'archives/news/{instance.pub_date}/{instance.slug}/{filename}'

    photo_1 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", null=True, max_length=500)
    photo_2 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True, max_length=500)
    photo_3 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True, max_length=500)
    photo_4 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True, max_length=500)
    photo_5 = models.ImageField(upload_to=directory_path, verbose_name="Картинка новини", blank=True, null=True, max_length=500)
    objects = models.Manager()


    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['name']

    def __str__(self):
        return self.name

class Theses(models.Model):
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
    name = models.CharField(max_length=100, help_text='не більше ніж 100 символів',
                           verbose_name='Категорія')

    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', db_index=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name
