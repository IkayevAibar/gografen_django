# Generated by Django 3.0 on 2021-02-04 11:07

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledgebase',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to=app.models.content_file_name_knowledge, verbose_name='Файлы'),
        ),
    ]
