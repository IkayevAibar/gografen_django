from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
class appUser(AbstractUser):
    phone=models.CharField(max_length=15,null=True)
    fathername = models.CharField('father name', max_length=150, blank=True)
    gender_CHOICES = [
        (0, 'None'),
        (1, 'Male'),
        (2, 'Female'),
    ]
    gender = models.IntegerField(choices=gender_CHOICES,default=0)
    birth_date = models.DateField('Birth date',default= datetime.date.today )
    card = models.CharField(max_length=16,null=True)
    position = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=20,default="Kazakhstan")
    subdivison = models.CharField(max_length=20,null=True)
    lead_activity = models.DateTimeField(default=timezone.now)
    client_activity = models.DateTimeField('Активность клиента',null=True)
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)