# Generated by Django 3.1.5 on 2021-01-29 09:25

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210126_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school_logo_1',
            field=models.FileField(blank=True, null=True, upload_to=app.models.content_file_name, verbose_name='Лого 250x64'),
        ),
    ]