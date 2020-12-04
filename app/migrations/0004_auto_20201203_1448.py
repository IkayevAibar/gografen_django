# Generated by Django 3.0 on 2020-12-03 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_appuser_school_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='school_logo',
        ),
        migrations.AddField(
            model_name='appuser',
            name='school_logo_1',
            field=models.ImageField(blank=True, null=True, upload_to='logo', verbose_name='Лого 250x64'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='school_logo_2',
            field=models.ImageField(blank=True, null=True, upload_to='logo', verbose_name='Лого 16x16'),
        ),
    ]
