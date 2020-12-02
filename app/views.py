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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

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
    class Meta:
        model=appUser 
        fields = ('username', 'password1', 'password2',)


def register(request):
    if request.method == 'POST':
        f = appUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        f = UserCreationForm()

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
