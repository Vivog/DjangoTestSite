# Generated by Django 4.0.6 on 2022-08-16 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nio_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='description',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='number',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='year',
        ),
    ]