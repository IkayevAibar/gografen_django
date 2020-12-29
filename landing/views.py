from django.shortcuts import render,redirect
from datetime import datetime
import requests
from django.http import HttpRequest,HttpResponse

# Create your views here.
def mainpage(request):
    """Renders the main page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'landing/main.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


