# Generated by Django 3.0 on 2020-11-26 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='fathername',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='phone',
        ),
    ]