from datetime import datetime
from django.contrib import admin
from django.urls import include,path
from django.contrib.auth.views import LoginView, LogoutView
from app import views


urlpatterns = [
    path('',include('app.urls')),
]
