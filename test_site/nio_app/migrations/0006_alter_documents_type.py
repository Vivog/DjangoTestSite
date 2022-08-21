# Generated by Django 4.0.6 on 2022-08-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nio_app', '0005_remove_documents_slug_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='type',
            field=models.CharField(choices=[('M', 'Методики'), ('P', 'Паспорти'), ('KE', 'Керівництва з експлуатації'), ('TD', 'Техничні довідки'), ('ZT', 'Технічні звіти'), ('TI', 'Технологічні інструкції'), ('I', 'Інше'), (None, 'Тип')], help_text='Оберіть тип документу', max_length=50, verbose_name='Тип документу'),
        ),
    ]
