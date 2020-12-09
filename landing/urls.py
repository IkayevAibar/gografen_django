from django.urls import include,path
from django.contrib import admin
from landing import views
from gografen import settings
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from django.conf.urls.static import static

urlpatterns = [
    path('', views.mainpage, name='main'),
]
