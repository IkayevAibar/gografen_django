# Generated by Django 3.0 on 2020-12-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201202_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='school_logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Лого'),
        ),
    ]
