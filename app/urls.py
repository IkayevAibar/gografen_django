from django.urls import include,path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime


urlpatterns = [
    path('<int:pk>/',views.GetappUserView.as_view()),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
