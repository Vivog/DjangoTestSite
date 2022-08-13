# Generated by Django 4.0.6 on 2022-08-09 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nio_app', '0004_alter_divisions_boss'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publications',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Публікація', 'verbose_name_plural': 'Публікації'},
        ),
        migrations.AlterModelOptions(
            name='reviewsnews',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Відгук на новину', 'verbose_name_plural': 'Відгуки на новину'},
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(help_text='Введіть короткий опис мети новини', max_length=5000, null=True, verbose_name='Короткий опис'),
        ),
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(help_text='не більше 15 000 символів', max_length=15000, null=True, verbose_name='Текст новини'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='text',
            field=models.TextField(help_text='не більше 50 000 символів', max_length=50000, null=True, verbose_name='Текст публікації'),
        ),
        migrations.AlterField(
            model_name='reviewsnews',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nio_app.news', verbose_name='Новина'),
        ),
    ]