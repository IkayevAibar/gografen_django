from datetime import datetime
from django.contrib import admin
from django.urls import include,path
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from app import views
from gografen import settings
from django.conf.urls.static import static
from .views import wildcard_redirect 
urlpatterns = [
    url(r'^(?P<path>.*)', wildcard_redirect ,name='wildcard_r'),

]
