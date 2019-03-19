from .base import *
from .ldap import *
from .email import *

DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_USE_SSL = True

THIRD_PARTY_APPS += [
    'django_extensions'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
