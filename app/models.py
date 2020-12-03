from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class appUser(AbstractUser):
    class Meta:
        permissions = [
            ("can_add_comment","Can add comments"),
            ("can_edit_user_data","Can edit user data"),
        ]
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
    school_name = models.CharField('Школа',max_length=20,null=True,blank=True,unique=True)
    sub_domen = models.CharField('Домен',max_length=15,null=True,blank=True,unique=True)
    country = models.CharField('Страна',max_length=20,default="Kazakhstan",null=True)
    subdivison = models.CharField('Подразделение',max_length=20,null=True,blank=True)
    lead_activity = models.DateTimeField('Активность лида',default=timezone.now,null=True)
    client_activity = models.DateTimeField('Активность клиента',null=True)
    def __str__(self):
        return "%d | %s | %s %s" % (self.id,self.username, self.first_name, self.last_name)


class Course(models.Model):
    title = models.CharField('Название',max_length=20)
    cost = models.IntegerField('Стоимость',default=0,help_text='в тенге')
    poster = models.TextField('Постер',max_length=1000)
    short_desc = models.TextField('Короткое описание',max_length=200)
    full_desc = models.TextField('Полное описание',max_length=500)
    start_date = models.DateField('Начало даты',default= datetime.date.today)
    end_date = models.DateField('Конец даты')
    course_programm = models.CharField('Программа курса',max_length=30)
    duration = models.IntegerField('Длителность',default=0,help_text='в минутах')
    pub_date = models.DateTimeField('Дата публикации')
    creator_id = models.ForeignKey('appUser',on_delete=models.SET_NULL,blank=True,null=True,help_text='Создатель курса')
    def __str__(self):
        return "%s Price:%s tg" % (self.title, self.cost)

