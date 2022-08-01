# Generated by Django 4.0.6 on 2022-07-30 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nio_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='не більше ніж 100 символів', max_length=100, verbose_name='Теза')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
                ('photo', models.ImageField(upload_to='theses/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Теза',
                'verbose_name_plural': 'Тези',
            },
        ),
        migrations.AlterModelOptions(
            name='cooperation',
            options={'ordering': ['name'], 'verbose_name': 'Підрозділ взаємодії', 'verbose_name_plural': 'Підрозділи взаємодії'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['loc'], 'verbose_name': 'Приміщення', 'verbose_name_plural': 'Приміщення'},
        ),
        migrations.AddField(
            model_name='divisions',
            name='theses',
            field=models.ManyToManyField(to='nio_app.theses', verbose_name='Тези'),
        ),
    ]