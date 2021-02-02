from django.conf import settings
from django_hosts import patterns, host
from app import urls as app_urls
from landing import urls as l_urls

host_patterns = patterns('',
    host(r'(\A)', l_urls  , name='landing'),
    host(r'api', settings.ROOT_URLCONF, name='api'),
    host(r'(^.+)', app_urls , name='app'),
    # host(r'(?!www).*', app_urls , name='app'),
    # host(r'*', hc_urls  , name='wildcard'),
) 