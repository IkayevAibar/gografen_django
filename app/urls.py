from django.urls import include,path
from django.contrib import admin
from app import views
from gografen import settings
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from django.conf.urls.static import static

urlpatterns = [
    # path('auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    path('', views.mainpage, name='main'),
    path('login_token',views.login_by_token,name='login_by_token'),
    path('home', views.home, name='home'),
    path('admin/', admin.site.urls ,name='admin'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('users/', views.users, name='users'),
    path('profile/', views.profile, name='profile'),
    path('users/delete/<int:id>/', views.deluser, name='deluser'),
    path('users/deleted/<int:id>/', views.delduser, name='delduser'),
    path('users/editeduser/<int:id>/', views.editeduser, name='editeduser'),
    path('users/edit/<int:id>/', views.edituser, name='edituser'),
    path('roles/', views.roles, name='roles'),
    path('roles/add/', views.addrole, name='addrole'),
    path('roles/delete/<int:id>/', views.delrole, name='delrole'),
    # path('roles/edit/<int:id>/', views.editrole, name='editrole'),
    path('roles/deleted/<int:id>/', views.deldrole, name='deldrole'),
    path('users/add/', views.adduser, name='adduser'),
    path('catalog/', views.catalog, name='catalog'),
    path('vectors/', views.vectors, name='vectors'),
    path('vectors/add/', views.addvector, name='addvector'),
    path('vectors/<int:id>/', views.vector, name='vector'),
    path('vectors/<int:id>/edit', views.editvector, name='editvector'),
    path('courses/', views.courses, name='courses'),
    path('mycourses/', views.mycourses, name='mycourses'),
    path('courses/add/', views.addcourse, name='addcourse'),
    path('courses/<int:id>/', views.course, name='course'),
    path('courses/<int:id>/edit', views.editcourse, name='editcourse'),
    path('courses/delete/<int:id>/', views.delcourse, name='delcourse'),
    path('courses/deleted/<int:id>/', views.deldcourse, name='deldcourse'),
    path('courses/<int:id>/add', views.addlesson, name='addlesson'),
    path('courses/<int:id>/buy', views.buy, name='buy'),
    path('courses/<int:id>/lesson/<int:l_id>', views.lesson, name='lesson'),
    path('courses/<int:id>/lesson/delete/<int:l_id>', views.dellesson, name='dellesson'),
    path('courses/<int:id>/lesson/edit/<int:l_id>', views.editlesson, name='editlesson'),
    path('courses/<int:id>/lesson/deleted/<int:l_id>', views.deldlesson, name='deldlesson'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    # path('comments/', include('django_comments_xtd.urls')),
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
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(r'^favicon.ico$', document_root='media/logo/favicon.ico')
