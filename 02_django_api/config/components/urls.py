import os

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()
INTERNAL_IPS = os.environ.get('INTERNAL_IPS').split()


ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'
