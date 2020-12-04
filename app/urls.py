from django.urls import include,path
from app import views
from gografen import settings
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from django.conf.urls.static import static

urlpatterns = [
    # path('auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
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
if settings.DEBUG:
    urlpatterns += static(r'^favicon.ico$', document_root='media/logo/favicon.ico')