from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import os
from django.core.cache import cache 
from gografen import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
# from comment.models import Comment

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))

def content_file_name_logo(instance, filename):
    return os.path.join(str(instance.id),'logo',filename)

def content_file_name_courses(instance, filename):
    return os.path.join(str(instance.creator_id.school_id.id),'courses',str(instance.title)+"_"+str(instance.creator_id.school_id.id) ,filename)

def content_file_name_knowledge(instance, filename):
    if(instance.lesson_id):
        return os.path.join(str(instance.course_id.creator_id.school_id.id),'knowledgebase',str(instance.course_id.id),str(instance.lesson_id.id),filename)
    else:
        return os.path.join(str(instance.course_id.creator_id.school_id.id),'knowledgebase',str(instance.course_id.id),filename)

def get_upload_path(instance, filename):
    return os.path.join(
      "knowledge","school_%d" % instance.school_id.id, "user_%d" % instance.id,filename)

# Create your models here.

class appUser(AbstractUser):
    def has_group(user, group_name):
        return user.groups.filter(name=group_name).exists()
    
    email = models.EmailField(_('email address'), blank=True,null=True)
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
    # USERNAME_FIELD = 'identifier'
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class School(models.Model):
    fs = FileSystemStorage(location='/media/photos')
    school_name = models.CharField('Школа',max_length=20,null=True,blank=True,unique=True)
    sub_domen = models.CharField('Домен',max_length=30,null=True,blank=True,unique=True)
    school_logo_1 = models.FileField('Лого 250x64',upload_to=content_file_name_logo,blank=True, null=True)
    school_logo_2 = models.FileField('Лого 16x16',upload_to=content_file_name_logo,blank=True, null=True)
    creator_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Создатель школы')
    def __str__(self):
        return "%s" % (self.school_name)

class Comment(models.Model):
    user_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Комментатор')
    course_id = models.ForeignKey('Course',on_delete=models.SET_NULL,blank=True,null=True,help_text='Курс')
    pub_date = models.DateTimeField('Дата публикации',default= timezone.now)
    content = models.CharField('Контент',max_length=220,null=True,blank=True)
    def __str__(self):
        return "%s(%s):'%s'" % (self.user_id,self.course_id,self.content)

class Course(models.Model):
    title = models.CharField('Название',max_length=20)
    cost = models.IntegerField('Стоимость',default=0,help_text='в тенге')
    poster = models.FileField('Постер',upload_to=content_file_name_courses,blank=True, null=True)
    mini_poster = models.FileField('Мини Постер',upload_to=content_file_name_courses,blank=True, null=True)
    short_desc = models.TextField('Короткое описание',max_length=200,blank=True, null=True)
    full_desc = models.TextField('Полное описание',max_length=500,blank=True, null=True)
    lesson_count = models.IntegerField('Количество уроков',default=0,blank=True, null=True)
    start_date = models.DateField('Начало даты',default= datetime.date.today)
    end_date = models.DateField('Конец даты',blank=True, null=True)
    duration = models.IntegerField('Длителность',default=0,help_text='в минутах',blank=True, null=True)
    pub_date = models.DateTimeField('Дата публикации',default=timezone.now)
    creator_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Создатель курса')
    vector_id = models.ForeignKey('Vector',on_delete=models.SET_NULL,blank=True,null=True,help_text='Направление')
    # comments = GenericRelation(Comment)
    def update_num_lessons(self):
        self.lesson_count=Lesson.objects.filter(course_id=self).count()
        return self.save(update_fields=["lesson_count"])
    def update_duration(self):
        lessons = Lesson.objects.filter(course_id=self)
        c_dur = 0
        for l in lessons:
            c_dur+=l.duration
        self.duration=c_dur
        return self.save(update_fields=["duration"])
    def __str__(self):
        return "%s Price:%s tg" % (self.title, self.cost)

class Lesson(models.Model):
    title = models.CharField('Название',max_length=20)
    short_desc = models.TextField('Короткое описание',max_length=200,blank=True, null=True)
    full_desc = models.TextField('Полное описание',max_length=500,blank=True, null=True)
    files = models.FileField('Содержание урока',upload_to='lessons',blank=True, null=True)
    video = models.FileField('Содержание урока',upload_to='lessons',blank=True, null=True)
    duration = models.IntegerField('Длителность',default=0,help_text='в минутах',blank=True, null=True)
    pub_date = models.DateField('Дата публикации',default= datetime.date.today,blank=True)
    course_id = models.ForeignKey('Course',on_delete=models.SET_NULL,blank=True,null=True,help_text='курс')
    teacher_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Учитель курса')
    checked = models.BooleanField(_("Проверено?"),blank=True,null=True)
    # comments = GenericRelation(Comment)
    def __str__(self):
        return "%s" % (self.title)

class HomeWork(models.Model):
    title = models.CharField('Название',max_length=20,default="",blank=True, null=True)
    desc = models.TextField('Короткое описание',max_length=200,blank=True, null=True)
    files = models.FileField('Содержание ДЗ',storage=FileSystemStorage(location='hw'),blank=True, null=True)
    pub_date = models.DateField('Дата публикации',default= datetime.date.today,blank=True)
    lesson_id = models.ForeignKey('Lesson',on_delete=models.SET_NULL,blank=True,null=True,help_text='урок')
    course_id = models.ForeignKey('Course',on_delete=models.SET_NULL,blank=True,null=True,help_text='курс')
    student_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Ученик курса')
    def __str__(self):
        return "%s" % (self.title)
    def __unicode__(self):
       return self.title

class KnowledgeBase(models.Model):
    files = models.FileField('Файлы',upload_to=content_file_name_knowledge,blank=True, null=True)
    pub_date = models.DateField('Дата публикации',default= datetime.date.today,blank=True)
    lesson_id = models.ForeignKey('Lesson',on_delete=models.SET_NULL,blank=True,null=True,help_text='урок')
    course_id = models.ForeignKey('Course',on_delete=models.SET_NULL,blank=True,null=True,help_text='курс')
    

class Vector(models.Model):
    title = models.CharField('Название',max_length=20)
    short_desc = models.TextField('Короткое описание',max_length=200,blank=True, null=True)
    pub_date = models.DateField('Дата публикации',default= datetime.date.today,blank=True)
    course_count = models.IntegerField('Количество курсов',default=0,blank=True, null=True)
    creator_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Создатель курса')
    duration = models.IntegerField('Длителность',default=0,help_text='в минутах',blank=True, null=True)
    def update_num_courses(self):
        self.course_count=Course.objects.filter(vector_id=self).count()
        return self.save(update_fields=["course_count"])
    def update_duration(self):
        cs = Course.objects.filter(vector_id=self)
        v_dur = 0
        for c in cs:
            v_dur+=c.duration
        self.duration=v_dur
        return self.save(update_fields=["duration"])
    def __str__(self):
        return "%s" % (self.title)

class Course_user(models.Model):
    course_id = models.ForeignKey('Course',on_delete=models.SET_NULL,blank=True,null=True,help_text='курс')
    student_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Ученик курса')
    start_date = models.DateField('Начало даты',default= datetime.date.today)
    end_date = models.DateField('Конец даты',blank=True, null=True)
    activity = models.DateTimeField('Активность клиента',null=True,blank=True)
    def __str__(self):
        return "%s|%s" % (self.student_id.username,self.course_id.title)