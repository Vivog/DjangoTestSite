# Generated by Django 4.0.6 on 2022-08-04 10:06

from django.db import migrations, models
import nio_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('nio_app', '0012_alter_divisions_photo_2_alter_divisions_photo_3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='photo_1',
            field=models.ImageField(null=True, upload_to=nio_app.models.Projects.directory_path, verbose_name='Картинка проекту'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='photo_2',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Projects.directory_path, verbose_name='Картинка проекту'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='photo_3',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Projects.directory_path, verbose_name='Картинка проекту'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='photo_4',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Projects.directory_path, verbose_name='Картинка проекту'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='photo_5',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Projects.directory_path, verbose_name='Картинка проекту'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='photo_1',
            field=models.ImageField(null=True, upload_to=nio_app.models.Publications.directory_path, verbose_name='Картинка публікації'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='photo_2',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Publications.directory_path, verbose_name='Картинка публікації'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='photo_3',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Publications.directory_path, verbose_name='Картинка публікації'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='photo_4',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Publications.directory_path, verbose_name='Картинка публікації'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='photo_5',
            field=models.ImageField(blank=True, null=True, upload_to=nio_app.models.Publications.directory_path, verbose_name='Картинка публікації'),
        ),
    ]
