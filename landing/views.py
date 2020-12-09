from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse

# Create your views here.
def mainpage(request):
    """Renders the main page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'landing/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


