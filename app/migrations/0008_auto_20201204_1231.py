# Generated by Django 3.0 on 2020-12-04 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20201204_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
