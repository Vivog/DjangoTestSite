# Generated by Django 4.0.6 on 2022-09-02 13:47

from django.db import migrations, models
import django.db.models.deletion
import projects.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        ('divisions', '0001_initial'),
        ('nio_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='не більше ніж 200 символів', max_length=200, verbose_name='Назва проекту')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('description', models.TextField(help_text='Введіть короткий опис мети проекту', max_length=5000, verbose_name='Опис підрозділу')),
                ('author', models.ManyToManyField(help_text='Оберіть автора/авторів проекту', to='staff.staff', verbose_name='Автор')),
                ('category', models.ManyToManyField(help_text='оберіть категорію/категорії', to='nio_app.categories', verbose_name='Оберіть категорію')),
                ('div', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='divisions.divisions', verbose_name='Назва підрозділу')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекти',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProjectsPics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, max_length=500, null=True, upload_to=projects.models.ProjectsPics.directory_path, verbose_name='Картинка проекту')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.projects', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Картинка проекту',
                'verbose_name_plural': 'Картинки проектів',
                'ordering': ['project'],
            },
        ),
        migrations.CreateModel(
            name='ProjectsDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(blank=True, max_length=500, null=True, upload_to=projects.models.ProjectsDocs.directory_path)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.projects', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Документ проекту',
                'verbose_name_plural': 'Документи проектів',
                'ordering': ['project'],
            },
        ),
        migrations.AddField(
            model_name='projects',
            name='docs',
            field=models.ManyToManyField(to='projects.projectsdocs', verbose_name='Документ до проекту'),
        ),
        migrations.AddField(
            model_name='projects',
            name='pics',
            field=models.ManyToManyField(to='projects.projectspics', verbose_name='Картинка до проекту'),
        ),
    ]