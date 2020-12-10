from django.conf import settings
from django_hosts import patterns, host
from app import urls as app_urls
from gografen.hostconf import urls as hc_urls
host_patterns = patterns('',
    host(r'api', settings.ROOT_URLCONF, name='api'),
    # host(r'(?!www).*', app_urls , name='app'),
    host(r'', app_urls  , name='app'),
    # host(r'*', hc_urls  , name='wildcard'),
) 