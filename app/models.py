from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import os
from django.core.cache import cache 
from gografen import settings
from django.contrib.auth.models import Group

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s" % ('favicon.ico',)
    return os.path.join('logo', filename)

# Create your models here.
class appUser(AbstractUser):
    def has_group(user, group_name):
        return user.groups.filter(name=group_name).exists()
    
    email = models.EmailField(_('email address'), blank=True, unique=True)
    phone=models.CharField('Сотовый',max_length=15,null=True,blank=True)
    fathername = models.CharField('Отчество', max_length=150, blank=True,null=True)
    gender_CHOICES = [
        (0, 'None'),
        (1, 'Male'),
        (2, 'Female'),
    ]
    gender = models.IntegerField('Пол',choices=gender_CHOICES,default=0)
    birth_date = models.DateField('Дата рождение',default= datetime.date.today,blank=True)
    card = models.CharField('Банковская карта',max_length=16,null=True,blank=True)
    position = models.CharField('Должность',max_length=20,null=True,blank=True)
    country = models.CharField('Страна',max_length=20,default="Kazakhstan",null=True)
    subdivison = models.CharField('Подразделение',max_length=20,null=True,blank=True)
    lead_activity = models.DateTimeField('Активность лида',default=timezone.now,null=True)
    client_activity = models.DateTimeField('Активность клиента',null=True,blank=True)
    school_id = models.ForeignKey('School',on_delete=models.SET_NULL,blank=True,null=True,help_text='Школа')
    is_online = models.BooleanField(default=False)
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class School(models.Model):
    school_name = models.CharField('Школа',max_length=20,null=True,blank=True,unique=True)
    sub_domen = models.CharField('Домен',max_length=30,null=True,blank=True,unique=True)
    school_logo_1 = models.FileField('Лого 250x64',upload_to='logo',blank=True, null=True)
    school_logo_2 = models.FileField('Лого 16x16',upload_to=content_file_name,blank=True, null=True)
    creator_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Создатель школы')
    def __str__(self):
        return "%s" % (self.school_name)


class Course(models.Model):
    title = models.CharField('Название',max_length=20)
    cost = models.IntegerField('Стоимость',default=0,help_text='в тенге')
    poster = models.TextField('Постер',max_length=1000,blank=True, null=True)
    mini_poster = models.TextField('Постер',max_length=1000,blank=True, null=True)
    short_desc = models.TextField('Короткое описание',max_length=200,blank=True, null=True)
    full_desc = models.TextField('Полное описание',max_length=500,blank=True, null=True)
    start_date = models.DateField('Начало даты',default= datetime.date.today)
    lesson_count = models.IntegerField('Количество уроков',default=0,blank=True, null=True)
    end_date = models.DateField('Конец даты',blank=True, null=True)
    duration = models.IntegerField('Длителность',default=0,help_text='в минутах',blank=True, null=True)
    pub_date = models.DateTimeField('Дата публикации',default= datetime.date.today)
    creator_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Создатель курса')
    def update_num_lessons(self):
        self.lesson_count=Lesson.objects.filter(course_id=self).count()
        return self.save(update_fields=["lesson_count"])
    def __str__(self):
        return "%s Price:%s tg" % (self.title, self.cost)

class Lesson(models.Model):
    
    title = models.CharField('Название',max_length=20)
    short_desc = models.TextField('Короткое описание',max_length=200,blank=True, null=True)
    full_desc = models.TextField('Полное описание',max_length=500,blank=True, null=True)
    duration = models.IntegerField('Длителность',default=0,help_text='в минутах',blank=True, null=True)
    files = models.FileField('Содержание урока',upload_to='lessons',blank=True, null=True)
    pub_date = models.DateField('Дата публикации',default= datetime.date.today)
    course_id = models.ForeignKey('Course',on_delete=models.SET_NULL,blank=True,null=True,help_text='курс')
    teacher_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Учитель курса')
    def __str__(self):
        return "%s" % (self.title)


