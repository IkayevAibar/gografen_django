from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from .serializers import GetappUserSerializer,GetappUserPublicSerializer,CreateappUserSerializer
# from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import appUser,Course,Lesson
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

class UserActivationView(APIView):
        def get (self, request):
            urlpathrelative=request.get_full_path()
            ABSOLUTE_ROOT= request.build_absolute_uri('/')[:-1].strip("/")

            spliturl=os.path.split(urlpathrelative)
            relpath=os.path.split(spliturl[0])
            uid=spliturl[0]
            uid=os.path.split(uid)[1]

            token=spliturl[1]
            postpath=ABSOLUTE_ROOT+relpath[0]+'/'
            post_data = [('uid', uid), ('token', token),]     
            result = urllib.request.urlopen(postpath, urllib.parse.urlencode(post_data).encode("utf-8"))
            content = result.read()
            return Response(content)

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

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     def perform_create(self, serializer):
#         created_object = serializer.save()
#         send_mail('Subject here','Here is the message.','from@example.com', 
#             [created_object.email],  fail_silently=False,)
@login_required
def home(request):
    """Renders the home page."""
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


class appUserSettingsChangeForm(forms.ModelForm):
    school_name = forms.CharField(max_length=100)
    sub_domen = forms.URLField(max_length=30,validators=[validate_gografen])
    school_logo_1 = forms.FileField()
    school_logo_2 = forms.FileField()
    
    class Meta:
        model=appUser 
        fields = ('school_name', 'sub_domen', 'school_logo_1','school_logo_2')

class appUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,error_messages={'name_length':"Слишком длинное имя"})
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(error_messages={'email_exists':'Email exists'})
    school_name = forms.CharField(max_length=100)
    sub_domen = forms.URLField(max_length=30,validators=[validate_gografen])
    phone = forms.CharField(max_length=20)
    
    class Meta:
        model=appUser 
        fields = ('username', 'password1', 'password2','first_name', 'last_name', 'email','school_name', 'sub_domen','phone')

class GroupCreationForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(label = "Права:", choices=Permission.objects.values_list('id', 'name'), widget = forms.CheckboxSelectMultiple)
    class Meta:
        model=Group 
        fields = ('name','description','permissions')
        


class appUserAddingForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,error_messages={'name_length':"Слишком длинное имя"})
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(error_messages={'email_exists':'Email exists'})
    phone = forms.CharField(max_length=20)
    role = forms.CharField(max_length=30)

    class Meta:
        model=appUser 
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'role')
 

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
                group_role = Group.objects.get(name='MainTeacher')
                user.groups.add(group_role)
                new_url = user.sub_domen.split('.')[0] + ".localhost:8000"
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
    g = Group.objects.all()
    if request.method == 'POST':
        form = appUserAddingForm(request.POST)
        if form.is_valid():
            newuser=form.save()
            group_role = Group.objects.get(name=form.data['role'])
            newuser.groups.add(group_role)
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

# @user_passes_test(lambda u: u.has_perm('app.view_appuser'),redirect_field_name='home')
@permission_required('app.view_appuser')
def users(request):
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

    

@permission_required('app.add_appuser')
def addrole(request):
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

@permission_required('auth.add_group')
def roles(request):
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
    


@login_required(login_url='/login/')
def settings(request):
    """Renders the settings page."""
    s=appUser.objects.filter(id=request.user.id)
    if request.method == 'POST':
        f = appUserSettingsChangeForm(request.POST, request.FILES, instance=request.user )
        if f.is_valid():
            f.save()
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
                    'sch_name': s[0].school_name,
                    'sch_domen': s[0].sub_domen,
                    'f':f
                }
            )
    else:
        f = appUserSettingsChangeForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/settings.html',
        {
            'title':'settings',
            'message':'Your settings page.',
            'year':datetime.now().year,
            'sch_name': s[0].school_name,
            'sch_domen': s[0].sub_domen,
            'f':f
        }
    )

   
    
    
@login_required
def contact(request):
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
