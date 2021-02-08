from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse, HttpResponseNotFound,HttpResponseRedirect
from django.utils import timezone
from .serializers import GetappUserSerializer,GetappUserPublicSerializer,CreateappUserSerializer
# from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Course_user, KnowledgeBase, Vector, appUser,Course,Lesson,School
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
from gografen.settings import MEDIA_ROOT
from rest_framework.authtoken.models import Token
import vimeo

# from django.contrib.auth.mixins import UserPassesTestMixin
# from django.contrib.auth.mixins import LoginRequiredMixin

def mainpage(request):
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
    print(request.get_host())
    sub_domain = request.get_host().split('.')[0]
    print(sub_domain)
    user_school = request.user.school_id.sub_domen
    if(user_school == (sub_domain+".gografen.com")):
        school = School.objects.filter(sub_domen=request.user.school_id.sub_domen)[0]
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
    else:
        return redirect('logout')
from django.utils.datastructures import MultiValueDict as MVD
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def login_by_token(request):
    sub_domain = request.get_host().split('.')[0]
    token_user = Token.objects.get_or_create(key=MVD(request.GET)['token'])
    # print(token_user[0].user.id)
    user = appUser.objects.filter(id=token_user[0].user.id).first()
    login(request,user)
    # user = authenticate(username=user.username, password=user.password)
    if user is not None:
        return redirect('home')
    else:
        return redirect('login')




def register(request):
    new_url = "http://localhost:8000"
    sub_domain = request.get_host().split('.')[0]
    if(request.get_host().split('.')[0] == 'localhost:8000'):
        if request.method == 'POST':
            f = appUserCreationForm(request.POST)
            
            if f.is_valid():
                user=f.save()
                try:
                    send_mail('Test', 'Message', 'gografen@test.com', user.email)
                except Exception:
                    pass
                school = School(sub_domen = str(user.id)+".gografen.com", school_name = user.first_name,creator_id=user)
                school.save()
                user.school_id = school
                group_role = Group.objects.get(name='MainTeacher')
                user.groups.add(group_role)
                user.save(update_fields=["school_id"])
                new_url = "http://"+ str(user.id) + ".localhost:8000"
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

@permission_required('app.add_appuser')
def adduser(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.all()
        if request.method == 'POST':
            form = appUserAddingForm(request.POST)
            if form.is_valid():
                newuser=form.save()
                group_role = Group.objects.get(name=form.data['role'])
                newuser.groups.add(group_role)
                newuser.school_id = request.user.school_id
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
                        'form':form,
                        'school':school,
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
                'form':form,
                'school':school,

            }
        )
    else:
        return redirect('main')

@permission_required('app.view_appuser')
def users(request):
    # per = Permission.objects.all()
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the users page."""
        school_ = School.objects.filter(sub_domen=(sub_domain+".gografen.com"))
        users = appUser.objects.filter(school_id=school_[0])
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/users.html',
            {
                'title':'Users',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'users':users,
                'school':school,

            }
        )
    else:
        return redirect('main')

@login_required
def profile(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the users page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/profile.html',
            {
                'title':'Profile',
                'message':'Your profile page.',
                'year':datetime.now().year,
                'school':school,

            }
        )
    else:
        return redirect('main')


@permission_required('app.delete_appuser')
def deluser(request,id):
    per = Permission.objects.all()
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        u = appUser.objects.filter(id=id)[0]
        candel = True
        print(per[6].codename)
        if(u.id==request.user.id):
            candel=False
        if(u.school_id!=request.user.school_id or u.id==2):
            return redirect('users')
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/deluser.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'candel':candel,
                'u':u,
            }
        )
    else:
        return redirect('main')

@permission_required('app.delete_appuser')
def delduser(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        u = appUser.objects.filter(id=id)[0]
        if(u.id==request.user.id or u.school_id!=request.user.school_id or u.id==2):
            return redirect('users')
        u.delete()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return redirect('users')
    else:
        return redirect('main')

@login_required
def edituser(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        u = appUser.objects.filter(id=id)[0]
        candel = True
        # if(u.id==request.user.id):
            # candel=False
        can=False
        if(id!=request.user.id):
            for perm in request.user.groups.all()[0].permissions.all():
                if(perm.name=='Can change user'):
                    can=True
            if(can==False or u.school_id!=request.user.school_id or u.id==2):
                return redirect('home')
        if request.method == 'POST':
            form = appUserChangeForm(request.POST)
            if form.is_valid():
                u.first_name = form.data['first_name']
                u.last_name = form.data['last_name']
                u.fathername = form.data['fathername']
                if(u.email!=form.data['email']):
                    mailcheck=appUser.objects.filter(email=form.data['email'])
                    if(mailcheck.count()>0):
                        m = messages.error(request, 'Email is already exist.')
                        assert isinstance(request, HttpRequest)
                        return render(
                            request,
                            'app/edituser.html',
                            {
                                'title':'Adding Lesson',
                                'message':'Your application description page.',
                                'year':datetime.now().year,
                                'school':school,
                                'candel':candel,
                                'u':u,
                                'messages':m,
                                'form':form,
                            }
                        )
                    else:
                        u.email = form.data['email']
                        
                u.phone = form.data['phone']
                u.gender = form.data['gender']
                u.birth_date = form.data['birth_date']
                u.country = form.data['country']
                u.save(update_fields=['first_name','last_name','fathername','birth_date','email','phone','gender','country'])
                return redirect('users')
            else:
                m = messages.error(request, 'Form invalid.')
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/edituser.html',
                    {
                        'title':'Adding Lesson',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'candel':candel,
                        'u':u,
                        'messages':m,
                        'form':form,
                    }
                )

        else:
            form = appUserChangeForm()
        """Renders the catalog page."""
        m = messages.error(request, 'Method is not Post.')
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/edituser.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'candel':candel,
                'u':u,
                'messages':m,
                'form':form,
            }
        )
    else:
        return redirect('main')

@login_required
def editeduser(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    can=False
    if(sub_domain != "localhost:8000"):
        u = appUser.objects.filter(id=id)[0]
        if request.method == 'POST':
            form = appUserChangeForm(request.POST)
            # print(form)
            if form.is_valid():
                form.save()
                for perm in request.user.groups.all()[0].permissions.all():
                    if(perm.name=='Can view user'):
                        can=True
                if(can==False):
                    return redirect('home')
                return redirect('users')
            else:
                assert isinstance(request, HttpRequest)
                m = messages.error(request, 'Form invalid.')
                return redirect('users')
        else:
            form = appUserChangeForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        m = messages.error(request, 'Method is not Post.')
        return redirect('users')
    else:
        return redirect('main')

@permission_required('app.add_appuser')
def addrole(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.all()
        counter=0
        p = Permission.objects.all().exclude(name="Can change session").exclude(name="Can add session").exclude(name="Can delete session").exclude(name="Can view session").exclude(name="Can change content type").exclude(name="Can add content type").exclude(name="Can delete content type").exclude(name="Can view content type").exclude(name="Can change log entry").exclude(name="Can add log entry").exclude(name="Can delete log entry").exclude(name="Can view log entry").exclude(name="Can delete site").exclude(name="Can view site").exclude(name="Can change site").exclude(name="Can add site")
        count = {}
        # print(p)
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
                        'school':school,
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
                'school':school,

            }
        )
    else:
        return redirect('main')
    

@permission_required('auth.add_group')
def roles(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        """Renders the roles page."""
        school_ = School.objects.filter(sub_domen=(sub_domain+".gografen.com"))
        users = appUser.objects.filter(school_id=school_[0])
        g = Group.objects.all()
        g_c = {}
        for gr in g:
            count = 0
            for user in users:
                if(user.has_group(gr)):
                    count+=1
            g_c[gr]=count
        # print(g_c)
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/roles.html',
            {
                'title':'Roles',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'counts':g_c,
            }
        )
    else:
        return redirect('main')
    



@login_required(login_url='/login/')
def settings(request):
    print(MEDIA_ROOT)
    school = School.objects.filter(id=request.user.school_id.id)[0]
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
                new_url = "http://" + school.sub_domen.split('.')[0] + ".localhost:8000"
                return HttpResponseRedirect(new_url)
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
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        courses = Course.objects.all()
        list_=[]
        for course in courses:
            if(request.user.school_id == course.creator_id.school_id):
                list_.append(course)
        for c in list_:
            c.update_num_lessons()
            c.update_duration()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/catalog.html',
            {
                'title':'Catalog',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'courses':list_,
            }
        )
    else:
        return redirect('main')

@login_required
def vectors(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        vectors = Vector.objects.all()
        list_=[]
        for vector in vectors:
            print(vector.creator_id.school_id)
            if(request.user.school_id == vector.creator_id.school_id):
                # access = Course_user.objects.filter(course_id=course,student_id=request.user).first()
                # print(access)
                # if(access):
                list_.append(vector)
        for v in list_:
            v.update_num_courses()
            v.update_duration()
        """Renders the courses page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/vectors.html',
            {
                'title':'Courses',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'vectors':list_,
            }
        )
    else:
        return redirect('main')


@permission_required('app.add_course')
def addvector(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        
        if request.method == 'POST':
            form = VectorAddForm(request.POST)
            if form.is_valid():
                print(form.data)
                form.save()
                return redirect('vectors')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addvector.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                    }
                )
        else:
            form = VectorAddForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/addvector.html',
            {
                'title':'Adding Course',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'form':form,
            }
        )
    else:
        return redirect('main')
  

@login_required
def homework(request,id,l_id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        course = Course.objects.filter(id=id).first()
        access = Course_user.objects.filter(course_id=course,student_id=request.user)
        is_sent = HomeWork.objects.filter(student_id=request.user,course_id=course,lesson_id=Lesson.objects.filter(id=l_id).first())
        print(is_sent)
        if(is_sent.count()>0):
            return redirect('lesson',id,l_id)
        if(request.user.school_id != course.creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        if(request.method=="POST"):
            form = HomeworkAddForm(request.POST)
            if form.is_valid():
                # print(form.data)
                form.save()
                return redirect('lesson',id,l_id)
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addhomework.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                        'c_id':id,
                        'l_id':Lesson.objects.filter(id=l_id).first()
                    }
                )
        else:
            form = HomeworkAddForm()


        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/addhomework.html',
            {
                'title':'homework ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'form':form,
                'c_id':id,
                'l_id':Lesson.objects.filter(id=l_id).first()
            }
        )
    else:
        return redirect('main')


@login_required
def edithomework(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        vector = Vector.objects.filter(id=id).first()
        if(request.user.school_id != vector.creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        """Renders the courses page."""
        if request.method == 'POST':
            form = VectorAddForm(request.POST)
            if form.is_valid():
                print(form.data)
                # form.save()
                vector.title = form.data['title']
                vector.short_desc = form.data['short_desc']
                vector.creator_id = appUser.objects.get(id=form.data['creator_id'])

                vector.save(update_fields=["title","short_desc","creator_id"])
                return redirect('vectors')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/edithomework.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                    }
                )
        else:
            form = VectorAddForm()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/edithomework.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'vector':vector,
                'form':form,
            }
        )
    else:
        return redirect('main')


@login_required
def vector(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        vector = Vector.objects.filter(id=id).first()
        if(request.user.school_id != vector.creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/vector.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'vector':vector,
            }
        )
    else:
        return redirect('main')


@login_required
def editvector(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        vector = Vector.objects.filter(id=id).first()
        if(request.user.school_id != vector.creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        """Renders the courses page."""
        if request.method == 'POST':
            form = VectorAddForm(request.POST)
            if form.is_valid():
                print(form.data)
                # form.save()
                vector.title = form.data['title']
                vector.short_desc = form.data['short_desc']
                vector.creator_id = appUser.objects.get(id=form.data['creator_id'])

                vector.save(update_fields=["title","short_desc","creator_id"])
                return redirect('vectors')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/editvector.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                    }
                )
        else:
            form = VectorAddForm()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/editvector.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'vector':vector,
                'form':form,
            }
        )
    else:
        return redirect('main')



@login_required
def courses(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        courses = Course.objects.all()
        list_=[]
        for course in courses:
            # print(course.creator_id.school_id)
            if(request.user.school_id == course.creator_id.school_id):
                if(course.creator_id == request.user or course.creator_id.school_id.creator_id == request.user):
                    list_.append(course)
        for c in list_:
            c.update_num_lessons()
            c.update_duration()
        """Renders the courses page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/courses.html',
            {
                'title':'Courses',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'courses':list_,
            }
        )
    else:
        return redirect('main')

@login_required
def mycourses(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        courses = Course.objects.all()
        list_=[]
        for course in courses:
            print(course.creator_id.school_id)
            if(request.user.school_id == course.creator_id.school_id):
                access = Course_user.objects.filter(course_id=course,student_id=request.user).first()
                print(access)
                if(access):
                    list_.append(course)
        for c in list_:
            c.update_num_lessons()
            c.update_duration()
        """Renders the courses page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/mycourses.html',
            {
                'title':'Courses',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'courses':list_,
            }
        )
    else:
        return redirect('main')



@login_required
def course(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    comments = Comment.objects.filter(course_id=id)
    if(sub_domain != "localhost:8000"):
        course = Course.objects.filter(id=id)
        access = Course_user.objects.filter(course_id=id,student_id=request.user).first()
        lessons = Lesson.objects.filter(course_id=course[0])
        if(request.user.school_id != course[0].creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        """Renders the courses page."""
        if request.method == 'POST':
            form = CommentAddForm(request.POST)
            if(form.data.get('edit')):
                comment = Comment.objects.filter(id=int(form.data.get('edit'))).first()
                comment.content=form.data.get('content')
                comment.save(update_fields=['content'])
            elif form.is_valid():
                form.save()
                
                return redirect('course',id)
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/course.html',
                    {
                        'title':'Course ',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school': school,
                        'course':course[0],
                        'lessons':lessons,
                        'comments':comments,
                        'access':access,
                    }
                )
        else:
            form = CommentAddForm()
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/course.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'course':course[0],
                'lessons':lessons,
                'comments':comments,
                'access':access,
                'form':form,
            }
        )
    else:
        return redirect('main')

@login_required
def editcourse(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        course = Course.objects.filter(id=id).first()
        lessons = Lesson.objects.filter(course_id=course)
        if(request.user.school_id != course.creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        """Renders the courses page."""
        print(request.method)
        if request.method == 'POST':
            form = CourseAddForm(request.POST,request.FILES, instance=request.user)
            if form.is_valid():
                print(request.FILES)
                # form.save()
                course.title = form.data['title']
                course.cost = form.data['cost']
                course.poster = request.FILES.get('poster', None)
                course.mini_poster = request.FILES.get('mini_poster', None)
                course.short_desc = form.data['short_desc']
                course.full_desc = form.data['full_desc']
                course.end_date = form.data['end_date']

                course.save(update_fields=["title","cost","poster","mini_poster","short_desc","full_desc","end_date"])
                
                return redirect('courses')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/editcourse.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'course':course,
                        'form':form,
                        'lessons':lessons,
                    }
                )
        else:
            form = CourseAddForm()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/editcourse.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'course':course,
                'form':form,
                'lessons':lessons,
            }
        )
    else:
        return redirect('main')



@permission_required('app.add_course')
def addcourse(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    vectors= Vector.objects.filter()
    if(sub_domain != "localhost:8000"):
        school_teachers = appUser.objects.filter(groups=(Group.objects.filter(name="Teacher")[0]),school_id=school.id)

        list_=[]
        for vector in vectors:
            if(request.user.school_id == vector.creator_id.school_id):
                list_.append(vector)
        
        if request.method == 'POST':
            form = CourseAddForm(request.POST,request.FILES, instance=request.user)
            if form.is_valid():
                # form.save()
                course = Course()
                course.title = form.data['title']
                course.cost = form.data['cost']
                course.poster = request.FILES.get('poster', None)
                course.mini_poster = request.FILES.get('mini_poster', None)
                course.short_desc = form.data['short_desc']
                course.full_desc = form.data['full_desc']
                course.end_date = form.data['end_date']
                course.creator_id = school_teachers.filter(id=form.data['creator_id']).first()
                course.vector_id = vectors.filter(id=form.data['vector_id']).first()
                course.save()
                
                # kb = KnowledgeBase.objects.create(
                #     course_id = course,
                #     files = request.FILES.get('poster', None)
                # )

                # kb2 = KnowledgeBase.objects.create(
                #     course_id = course,
                #     files = request.FILES.get('mini_poster', None)
                # )

                

                return redirect('courses')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addcourse.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                        'vectors':list_,
                        'teachers':school_teachers,
                    }
                )
        else:
            form = CourseAddForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/addcourse.html',
            {
                'title':'Adding Course',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'form':form,
                'vectors':list_,
                'teachers':school_teachers,

            }
        )
    else:
        return redirect('main')
  


@login_required
def buy(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        course = Course.objects.filter(id=id).first()
        access = Course_user.objects.filter(course_id=course,student_id=request.user)
        if(request.user.school_id != course.creator_id.school_id):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        """Renders the courses page."""
        if(request.method=="POST"):
            Course_user.objects.get_or_create(course_id=course,student_id=request.user,activity=timezone.now())
            user = appUser.objects.get(id=request.user.id)
            user.client_activity = timezone.now()
            user.save(update_fields=["client_activity"])

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/transaction.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'course':course,
                'access':access,
            }
        )
    else:
        return redirect('main')


@permission_required('app.delete_course')
def delcourse(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        course = Course.objects.filter(id=id)[0]
        lessons = Lesson.objects.filter(course_id=course)
        if(request.user.school_id != course.creator_id.school_id):
            return redirect('courses')
        """Renders the courses page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/delcourse.html',
            {
                'title':'Deleting Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'course':course,
                'lessons':lessons
            }
        )
    else:
        return redirect('main')


@permission_required('app.delete_course')
def deldcourse(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        course = Course.objects.filter(id=id).first()
        lessons = Lesson.objects.filter(course_id=course)
        kb = KnowledgeBase.objects.filter(course_id = course , pub_date = course.pub_date ).first()
        kb2 = KnowledgeBase.objects.filter(course_id = course , pub_date = course.pub_date ).first()
        if(request.user.school_id != course.creator_id.school_id):
            return redirect('courses')
        
        kb.delete()
        kb2.delete()
        course.delete()
        if(lessons.count()>0):
            for lesson in lessons:
                if(lesson!=None):
                    lesson.delete()
        return redirect('courses')
    else:
        return redirect('main')


@login_required
def lesson(request,id,l_id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        lesson = Lesson.objects.filter(id=l_id)
        lessons = Lesson.objects.filter(course_id=lesson[0].course_id)
        is_sent = HomeWork.objects.filter(student_id=request.user,course_id=Course.objects.filter(id=id).first(),lesson_id=Lesson.objects.filter(id=l_id).first())
        
        if(request.user.school_id != lesson[0].course_id.creator_id.school_id):
            return redirect('courses')
        
        access = Course_user.objects.filter(course_id=id,student_id=request.user)
        l = request.user.groups.values_list('name',flat = True).first()
        if(access.count()<1 and l!='MainTeacher' and l!='Teacher'):
            return redirect('course',id)
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/lesson.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'c_id':lesson[0].course_id,
                'lesson':lesson[0],
                'lessons':lessons,
                'access' : access,
                'is_sent':is_sent
            }
        )
    else:
        return redirect('main')

@login_required
def dellesson(request,id,l_id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        lesson = Lesson.objects.filter(id=l_id)
        if(request.user.school_id != lesson[0].course_id.creator_id.school_id):
            return redirect('courses')
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/dellesson.html',
            {
                'title':'Course ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'c_id':id,
                'lesson':lesson[0],
            }
        )
    else:
        return redirect('main')

def deldlesson(request,id,l_id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        lesson = Lesson.objects.filter(id=l_id)
        if(request.user.school_id != lesson[0].course_id.creator_id.school_id):
            return redirect('courses')
        lesson.delete()
        return redirect('course',id)
    else:
        return redirect('main')

def editlesson(request,id,l_id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    school_teachers = appUser.objects.filter(groups=(Group.objects.filter(name="Teacher")[0]),school_id=school.id)
    if(sub_domain != "localhost:8000"):
        if request.method == 'POST':
            form = LessonAddForm(request.POST,request.FILES or None,instance=request.user)
            print(form)
            if form.is_valid():
                # form.save()
                lesson = Lesson.objects.filter(id=l_id).first()
                lesson.title = form.data['title']
                lesson.files = request.FILES.get('files', None)
                lesson.short_desc = form.data['short_desc']
                lesson.full_desc = form.data['full_desc']
                lesson.duration = form.data['duration']
                lesson.teacher_id = appUser.objects.get(id=form.data['teacher_id'])
                lesson.course_id = Course.objects.get(id=form.data['course_id'])

                lesson.save(update_fields=['title', 'files','short_desc', 'full_desc','duration','teacher_id','course_id'])
                return redirect('course',id)
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/editlesson.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                        'teachers':school_teachers,
                    }
                )
        else:
            form = LessonAddForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/editlesson.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'form':form,
                'teachers':school_teachers,
            }
        )
    else:
        return redirect('main')
 

@permission_required('app.add_lesson')
def addlesson(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    school_teachers = appUser.objects.filter(groups=(Group.objects.filter(name="Teacher")[0]),school_id=school.id)
    v = vimeo.VimeoClient(token='35420b200bb4b36c2323ba71f3b95352',
                            key='b3fd03bb2e3ec1a808cbbf0a2eba71179e6309a2',
                            secret='VBdIoArUuMZlte7jj0OvznNqVQuHFoBFJJ1NvbDwnWc44Fjls2xOBRCa4rY0PcCS+9Qa3VXA+jdXJ+MRPQKsW1JHZLV+9jlk0sb51qUvpjvxz5vp2eIZrtFIymDPUWwe'
                            )
    
    if(sub_domain != "localhost:8000"):
        print(request.method)
        if(request.method == 'POST'):
            form = LessonAddForm(request.POST,request.FILES or None)
            print(form.data)
            if form.is_valid():
                print(request.FILES)
                lesson = form.save()
                # print(lesson.video.path)
                # v.upload(lesson.video.path)
                return redirect('course',id)
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addlesson.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'course_id':id,
                        'school':school,
                        'form':form,
                        'teachers':school_teachers,
                    }
                )
        else:
            form = LessonAddForm()
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/addlesson.html',
                {
                    'title':'Adding Lesson',
                    'message':'Your application description page.',
                    'year':datetime.now().year,
                    'course_id':id,
                    'school':school,
                    'form':form,
                    'teachers':school_teachers,
                }
            )
    else:
        return redirect('main')
  
@permission_required('auth.delete_group')
def delrole(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.filter(id=id)[0]
        candel = True
        print(g.id)
        if(g.id==1 or g.id==2 or g.id==3):
            candel=False

        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/delrole.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'candel':candel,
                'role':g,
            }
        )
    else:
        return redirect('main')

@permission_required('auth.change_group')
def editrole(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.filter(id=id)[0]
        candel = True
        counter=0
        p = Permission.objects.all().exclude(name="Can change session").exclude(name="Can add session").exclude(name="Can delete session").exclude(name="Can view session").exclude(name="Can change content type").exclude(name="Can add content type").exclude(name="Can delete content type").exclude(name="Can view content type").exclude(name="Can change log entry").exclude(name="Can add log entry").exclude(name="Can delete log entry").exclude(name="Can view log entry").exclude(name="Can delete site").exclude(name="Can view site").exclude(name="Can change site").exclude(name="Can add site")
        count = {}
        for pp in p:
            count[counter]=pp
            counter+=1
        if(g.id==1 or g.id==2 or g.id==3):
            candel=False
        if request.method == 'POST':
            form = GroupChangeForm(request.POST)
            

            if form.is_valid():
                # g = form.save()
                # g.name = form.data['name']
                # g.description = form.data['description']
                
                # g.permissions.set(form.data['permissions'])
                # g.save(update_fields=['name','description','permissions'])
                return redirect('courses')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/editrole.html',
                    {
                        'list':count,
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                        'role':g,
                    }
                )
        else:
            form = CourseAddForm()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/editrole.html',
            {
                'list':count,
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'candel':candel,
                'role':g,
            }
        )
    else:
        return redirect('main')

@permission_required('auth.delete_group')
def deldrole(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        g = Group.objects.filter(id=id)[0]
        if(g.id==1 or g.id==2 or g.id==3):
            return redirect('roles')
        g.delete()
        """Renders the catalog page."""
        assert isinstance(request, HttpRequest)
        return redirect('roles')
    else:
        return redirect('main')


@login_required
def allcomments(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        list_ = []
        comments = Comment.objects.all()
        if(comments.count()>0):
            for c in comments:
                print(c.user_id)
                if(c!=None):
                    if(c.user_id.school_id==request.user.school_id):
                        if(c.course_id.creator_id.school_id.creator_id == request.user):
                            list_.append(c)
                        elif(c.course_id.creator_id == request.user):
                            list_.append(c)
                        elif(c.user_id == request.user):
                            list_.append(c)


        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/allcomments.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'cc':list_,
            }
        )
    else:
        return redirect('main')

@login_required
def delcomment(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        comment = Comment.objects.filter(id=id).first()
        if(request.user.school_id != comment.user_id.school_id):
            return redirect('allcomments')
        comment.delete()
        assert isinstance(request, HttpRequest)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('main')

@login_required
def delhw(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        hws = HomeWork.objects.filter(student_id=request.user).first()  
        if(request.user.school_id != hws.student_id.school_id):
            return redirect('allhw')
        hws.delete()
        assert isinstance(request, HttpRequest)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('main')



@permission_required('app.view_homework')
def allhw(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        list_ = []
        hws = HomeWork.objects.filter(student_id=request.user)
        l = request.user.groups.values_list('name',flat = True).first()
        hwd = HomeWork.objects.all()
        if(l=='MainTeacher'):
            for hw in hwd:
                if hw.course_id.creator_id.school_id == request.user.school_id:
                    list_.append(hw)
        else:
            for hw in hwd:
                print(hw.course_id.creator_id == request.user)
                if hw.course_id.creator_id == request.user:
                    list_.append(hw)
        if(len(list_)>0):
            hws=list_


        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/myhws.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'hws':hws
            }
        )
    else:
        return redirect('main')

@login_required
def hw(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        hws = HomeWork.objects.filter(id=id).first()     
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/homework.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'hw':hws,
            }
        )
    else:
        return redirect('main')



@login_required
def edithw(request,id):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        hws = HomeWork.objects.filter(student_id=request.user,id=id).first()    
         
        if(request.method=="POST"):
            form = HomeworkAddForm(request.POST)
            if form.is_valid():
                print(form.data)
                # form.save()
                hws.title = form.data.get('title')
                hws.desc = form.data.get('desc')
                hws.files = form.data.get('files')
                hws.save(update_fields=["title","desc","files"])
                return redirect('allhw')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addhomework.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                        'c_id':hws.course_id.id,
                        'l_id':Lesson.objects.filter(id=hws.lesson_id.id).first()
                    }
                )
        else:
            form = HomeworkAddForm()

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/addhomework.html',
            {
                'title':'Adding Lesson',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school':school,
                'hw':hws,
                'form':form,
                'c_id':hws.course_id.id,
                'l_id':Lesson.objects.filter(id=hws.lesson_id.id).first()
            }
        )
    else:
        return redirect('main')

@login_required
def addhw(request):
    school = School.objects.filter(id=request.user.school_id.id)[0]
    sub_domain = request.get_host().split('.')[0]
    if(sub_domain != "localhost:8000"):
        access = Course_user.objects.filter(student_id=request.user)
        list_=[]
        list2 = []
        dict_ = {}
        for cu in access:
            course = Course.objects.filter(id=cu.course_id.id).first()
            list_.append(course)
            lessons = Lesson.objects.filter(course_id=course.id)
            for l in lessons:
                list2.append(l)
            dict_[course] = list2
            list2=[]
        
        
        # if(request.user.school_id != course.creator_id.school_id):
        #     return HttpResponseNotFound('<h1>Page not found</h1>')
        if(request.method=="POST"):
            form = HomeworkAddForm(request.POST)
            if form.is_valid():
                # print(request.FILES['files'])
                form.save()
                return redirect('allhw')
            else:
                assert isinstance(request, HttpRequest)
                return render(
                    request,
                    'app/addhw.html',
                    {
                        'title':'Adding Course',
                        'message':'Your application description page.',
                        'year':datetime.now().year,
                        'school':school,
                        'form':form,
                        'list':list_,
                        'dict':dict_
                    }
                )
        else:
            form = HomeworkAddForm()

        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/addhw.html',
            {
                'title':'homework ',
                'message':'Your application description page.',
                'year':datetime.now().year,
                'school': school,
                'form':form,
                'list':list_,
                'dict':dict_,
            }
        )
    else:
        return redirect('main')

