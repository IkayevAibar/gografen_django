from django.urls import include,path
from django.contrib import admin
from landing import views
from gografen import settings
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from django.conf.urls.static import static
from app import views as app_views

urlpatterns = [
    path('', views.mainpage, name='main'),
    path('register/', app_views.register, name='reg')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(r'^favicon.ico$', document_root='media/logo/favicon.ico')
