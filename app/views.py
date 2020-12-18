from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from .serializers import GetappUserSerializer,GetappUserPublicSerializer,CreateappUserSerializer
# from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import appUser,Course,Lesson,School
from rest_framework import permissions 
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.core.mail import send_mail
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission
import requests
from django import template
from django.contrib.auth.decorators import user_passes_test,permission_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    
from django.template import Context
from django.contrib.sites.models import Site
from django.urls import reverse
from app.forms import *

def mainpage(request):
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain == "localhost:8000"):
        return render(
                request,
                    'app/main.html',
                    {
                        'title':'Landing Page',
                        'year':datetime.now().year,
                    }
                )
    else:
        return redirect('home')


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.is_online = False
    user.save()

def validate_gografen(value): 
    if ".gografen.com" in value: 
        return value 
    else: 
        raise ValidationError("This field should have gogafen.com")

# class UserActivationView(APIView):
#     def get (self, request):
#         urlpathrelative=request.get_full_path()
#         ABSOLUTE_ROOT= request.build_absolute_uri('/')[:-1].strip("/")

#         spliturl=os.path.split(urlpathrelative)
#         relpath=os.path.split(spliturl[0])
#         uid=spliturl[0]
#         uid=os.path.split(uid)[1]

#         token=spliturl[1]
#         postpath=ABSOLUTE_ROOT+relpath[0]+'/'
#         post_data = [('uid', uid), ('token', token),]     
#         result = urllib.request.urlopen(postpath, urllib.parse.urlencode(post_data).encode("utf-8"))
#         content = result.read()
#         return Response(content)

class appUserView(ModelViewSet):
    #get user info to view
    serializer_class = GetappUserSerializer
    permission_classes= [permissions.IsAuthenticated]
    def get_queryset(self):
        return appUser.objects.filter(id=self.request.user.id)

class appUserPublicView(ModelViewSet):
    #get public user info to view
    queryset = appUser.objects.all()
    serializer_class = GetappUserPublicSerializer
    permission_classes= [permissions.AllowAny]

class appUserCreateView(ModelViewSet):
    serializer_class = CreateappUserSerializer
    permission_classes= [permissions.AllowAny]
    queryset = appUser.objects.all()


@login_required
def home(request):
    sub_domain = request.get_host().split('.')[0]
    school = School.objects.filter(creator_id=request.user)[0]
    if(sub_domain != "localhost:8000"):
        """Renders the home page."""
        return render(
            request,
            'app/index.html',
            {
                'school':school,
                'title':'Home Page',
                'year':datetime.now().year,
            }
        )
    else:
        new_url = "http://localhost:8000"
        return HttpResponseRedirect(new_url)


def register(request):
    new_url = "http://localhost:8000"
    sub_domain = request.get_host().split('.')[0]
    if(request.get_host().split('.')[0] == 'localhost:8000'):
        if request.method == 'POST':
            f = appUserCreationForm(request.POST)
            try:
                send_mail('Test', 'Message', 'gografen@test.com', user.email)
            except Exception:
                pass
            
            if f.is_valid():
                user=f.save()
                school = School(sub_domen = f.data['sub_domen'], school_name = f.data['school_name'],creator_id=user)
                school.save()
                new_url = "http://"+f.data['sub_domen'].split('.')[0] + ".localhost:8000"
                group_role = Group.objects.get(name='MainTeacher')
                user.school_id = school
                user.groups.add(group_role)
                user.save(update_fields=["school_id"])
                return HttpResponseRedirect(new_url)
            else:
                return render(request, 'app/register.html', {
                    'form': f,
                    'sub':sub_domain
                })
        else:
            f = appUserCreationForm()

        return render(request, 'app/register.html', {
            'form': f,
            'sub':sub_domain
        })
    else:
        return redirect('login')

    

# @user_passes_test(lambda u: u.has_perm('app.add_appuser'),redirect_field_name='home')
@permission_required('app.add_appuser')
def adduser(request):
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.all()
        if request.method == 'POST':
            form = appUserAddingForm(request.POST)
            if form.is_valid():
                newuser=form.save()
                group_role = Group.objects.get(name=form.data['role'])
                newuser.groups.add(group_role)
                newuser.school_id = request.user.school
                newuser.save(update_fields=["school_id"])
                return redirect('users')
            else:
                return render(
                    request,
                    'app/adduser.html',
                    {
                        'title':'Adding User',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'groups':g,
                        'form':form
                    }
                )
        else:
            form = appUserAddingForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/adduser.html',
            {
                'title':'Adding User',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'groups':g,
                'form':form
            }
        )
    else:
        return redirect('main')

# @user_passes_test(lambda u: u.has_perm('app.view_appuser'),redirect_field_name='home')
@permission_required('app.view_appuser')
def users(request):
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the users page."""
        users = appUser.objects.all()
        valid_users=[]  
        for user in users:
            if(user.sub_domen == request.user.sub_domen):
                if(user.has_group('Student') or user.has_group('MainTeacher') or user.has_group('Teacher')):
                        valid_users.append(user)
            
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/users.html',
            {
                'title':'Users',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'users':valid_users
            }
        )
    else:
        return redirect('main')
    

    

@permission_required('app.add_appuser')
def addrole(request):
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.all()
        counter=0
        p2 = Permission.objects.all()
        p = Permission.objects.all().exclude(name="Can change session").exclude(name="Can add session").exclude(name="Can delete session").exclude(name="Can view session").exclude(name="Can change content type").exclude(name="Can add content type").exclude(name="Can delete content type").exclude(name="Can view content type").exclude(name="Can change log entry").exclude(name="Can add log entry").exclude(name="Can delete log entry").exclude(name="Can view log entry")
        count = {}
        for pp in p:
            count[counter]=pp
            counter+=1
        if request.method == 'POST':
            form = GroupCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('roles')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addrole.html',
                    {
                        "list": count,
                        'title':'Adding Role',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'form':form,
                    }
                )
        else:
            form = GroupCreationForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/addrole.html',
            {
                "list": count,
                'title':'Adding Role',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'form':form,
            }
        )
    else:
        return redirect('main')
    

@permission_required('auth.add_group')
def roles(request):
    school = School.objects.filter(creator_id=request.user)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the roles page."""
        g = Group.objects.all()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/roles.html',
            {
                'title':'Roles',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'groups':g
            }
        )
    else:
        return redirect('main')
    

from gografen.settings import MEDIA_ROOT


@login_required(login_url='/login/')
def settings(request):
    print(MEDIA_ROOT)
    school = School.objects.filter(creator_id=request.user)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the settings page."""
        if request.method == 'POST':
            f = SchoolSettingsChangeForm(request.POST,request.FILES or None, instance=request.user)
            if f.is_valid():
                school.school_name = f.data['school_name']
                school.sub_domen = f.data['sub_domen']
                school.school_logo_1 = request.FILES.get('school_logo_1', None)
                school.school_logo_2 = request.FILES.get('school_logo_2', None)
                school.save(update_fields=["school_name","sub_domen","school_logo_1","school_logo_2"])
                print("You successfully updated the post")
                return redirect('home')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/settings.html',
                    {
                        'title':'settings',
                        'message':'Your settings page.',
                        'year':datetime.now().year,
                        'school': school,
                        'f':f,
                    }
                )
        else:
            f = SchoolSettingsChangeForm()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/settings.html',
            {
                'title':'settings',
                'message':'Your settings page.',
                'year':datetime.now().year,
                'school': school,
                'f':f,
            }
        )
    else:
        return redirect('main')

   
    
    
@login_required
def contact(request):
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the contact page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/contact.html',
            {
                'title':'Contact',
                'message':'Your contact page.',
                'year':datetime.now().year,
            }
        )
    else:
        return redirect('main')
@login_required
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
@login_required
def catalog(request):
    """Renders the catalog page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title':'Catalog',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

@login_required
def courses(request):
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        courses = Course.objects.all()
        for c in courses:
            c.update_num_lessons()
        """Renders the courses page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/courses.html',
            {
                'title':'Courses',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'courses':courses,
            }
        )
    else:
        return redirect('main')
