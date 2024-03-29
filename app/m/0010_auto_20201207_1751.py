# Generated by Django 3.0 on 2020-12-07 11:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_appuser_is_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_programm',
        ),
        migrations.AddField(
            model_name='course',
            name='mini_poster',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Постер'),
        ),
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.IntegerField(blank=True, default=0, help_text='в минутах', null=True, verbose_name='Длителность'),
        ),
        migrations.AlterField(
            model_name='course',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Конец даты'),
        ),
        migrations.AlterField(
            model_name='course',
            name='full_desc',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='course',
            name='poster',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Постер'),
        ),
        migrations.AlterField(
            model_name='course',
            name='pub_date',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='course',
            name='short_desc',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Короткое описание'),
        ),
    ]
