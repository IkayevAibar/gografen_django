# Generated by Django 3.0 on 2021-02-17 09:01

import app.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210208_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Название шаблона')),
                ('desc', models.TextField(blank=True, max_length=200, null=True, verbose_name='Условие упражнение')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст для упражнения')),
                ('files', models.FileField(blank=True, null=True, upload_to=app.models.content_file_name_hw, verbose_name='Содержание ДЗ')),
                ('creator_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='school',
            options={'verbose_name_plural': 'Школы'},
        ),
        migrations.AlterField(
            model_name='homework',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to=app.models.content_file_name_hw, verbose_name='Содержание ДЗ'),
        ),
        migrations.CreateModel(
            name='Exercise_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(blank=True, default=datetime.date.today, verbose_name='Дата публикации')),
                ('course_id', models.ForeignKey(blank=True, help_text='курс', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Course')),
                ('creator_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('ex_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Exercise')),
                ('lesson_id', models.ForeignKey(blank=True, help_text='урок', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Lesson')),
            ],
        ),
    ]
