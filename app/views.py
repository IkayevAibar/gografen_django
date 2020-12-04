from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest
from .serializers import GetappUserSerializer,GetappUserPublicSerializer,CreateappUserSerializer
# from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import appUser
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

import requests


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def request_user_activation(request, uid, token):
    """ 
    Intermediate view to activate a user's email. 
    """
    post_url = "http://127.0.0.1:8000/djoser_auth/users/activation/"
    post_data = {"uid": uid, "token": token}
    result = requests.post(post_url, data=post_data)
    content = result.text
    return Response(content)

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

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
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
        


def register(request):
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.first_name = self.first_name
    #     user.last_name = self.last_name
    #     user.set_password(self.cleaned_data["password1"])
    #     user.school_name = clean_school_name()
    #     user.email = clean_email()
    #     user.sub_domen = clean_sub_domen()
    #     # print(request.POST)
    #     if commit:
    #         user.save()
    #     return user
    
    if request.method == 'POST':
        f = appUserCreationForm(request.POST)
        try:
            send_mail('Test', 'Message', 'gografen@test.com', user.email)
        except Exception:
            pass
        
        if f.is_valid():
            f.save()
            
            # username = f.cleaned_data.get('username')
            # raw_password = f.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('login')
    else:
        f = appUserCreationForm()

    return render(request, 'app/register.html', {'form': f})

# class RegisterForm(request):
    
    
    

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

class appUserSettingsChangeForm(forms.ModelForm):
    
    
    school_name = forms.CharField(max_length=100)
    sub_domen = forms.URLField(max_length=30,validators=[validate_gografen])
    school_logo_1 = forms.FileField()
    school_logo_2 = forms.FileField()
    
    class Meta:
        model=appUser 
        fields = ('school_name', 'sub_domen', 'school_logo_1','school_logo_2')

@login_required(login_url='/login/')
def settings(request):
    """Renders the settings page."""
    s=appUser.objects.filter(id=request.user.id)
    print(s[0].school_logo_1)
    if request.method == 'POST':
        f = appUserSettingsChangeForm(request.POST, request.FILES, instance=request.user )
        if f.is_valid():
            f.save()
            return redirect('home')
        else:
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

