from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .serializers import GetappUserSerializer
from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from .models import appUser
from rest_framework import permissions 
class GetappUserView(RetrieveAPIView):
    #get user info to view
    queryset = appUser.objects.all()
    serializer_class = GetappUserSerializer

class UpdateappUserView(UpdateAPIView):
    # updating user info
    serializer_class = GetappUserSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        return appUser.objects.filter(id=self.request.user.id)
    


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

def register(request):
    """Renders the register page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/register.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

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
