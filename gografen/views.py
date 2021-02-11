from django.conf import settings
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseNotFound

DEFAULT_REDIRECT_URL = getattr(settings, "DEFAULT_REDIRECT_URL" , "http://api.localhost:8000")

def wildcard_redirect(request, path=None):
    new_url =  "http://api.localhost:8000/api/v1/1"
    print(path)
    print(request)
    # if path is not None:
    #     new_url = DEFAULT_REDIRECT_URL + "/" + path
    return HttpResponseRedirect(new_url)

def default(request):
    return HttpResponseNotFound('<h1>API</h1>')