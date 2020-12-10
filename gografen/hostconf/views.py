from django.conf import settings
from django.http import HttpResponseRedirect

DEFAULT_REDIRECT_URL = getattr(settings, "DEFAULT_REDIRECT_URL" , "http://localhost:8000")

def wildcard_redirect(request, path=None):
    new_url = DEFAULT_REDIRECT_URL
    print(path)
    print(request)
    if path is not None:
        new_url = DEFAULT_REDIRECT_URL + "/" + path
    return HttpResponseRedirect(new_url)