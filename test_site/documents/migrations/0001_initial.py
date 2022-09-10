# Generated by Django 4.0.6 on 2022-09-02 13:47

from django.db import migrations, models
import django.db.models.deletion
import documents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('divisions', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(help_text='Введіть рік випуску', max_length=4, null=True, verbose_name='Рік випуску')),
                ('number', models.CharField(help_text='Введіть номер документу', max_length=20, null=True, verbose_name='Номер документа')),
                ('name', models.CharField(help_text='Введіть назву документу', max_length=500, verbose_name='Назва документа')),
                ('description', models.TextField(help_text='Введіть короткий опис документа (мета)', max_length=5000, null=True, verbose_name='Опис документа')),
                ('slug', models.SlugField(max_length=500, unique=True, verbose_name='URL')),
                ('type', models.CharField(choices=[('M', 'Методики'), ('P', 'Паспорти'), ('KE', 'Керівництва з експлуатації'), ('TD', 'Техничні довідки'), ('ZT', 'Технічні звіти'), ('TI', 'Технологічні інструкції'), ('I', 'Інше'), (None, 'Тип')], help_text='Оберіть тип документу', max_length=50, verbose_name='Тип документу')),
                ('status', models.CharField(choices=[('Р', 'Розробка'), ('У', 'Узгодження'), ('В', 'Впроваджено'), (None, 'Статус')], help_text='Поточний статус документу', max_length=50, verbose_name='Статус документу')),
                ('doc', models.FileField(upload_to=documents.models.Documents.directory_path)),
                ('release_date', models.DateField(blank=True, help_text='Введіть дату впровадження', null=True, verbose_name='Дата впровадження')),
                ('author', models.ManyToManyField(help_text='Оберіть автора/авторів документу', related_name='authors', to='staff.staff', verbose_name='Автор')),
                ('div', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='div', to='divisions.divisions', verbose_name='Назва підрозділу')),
            ],
            options={
                'verbose_name': 'Документація',
                'verbose_name_plural': 'Документація',
                'ordering': ['-release_date'],
            },
        ),
    ]