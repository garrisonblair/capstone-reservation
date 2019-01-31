from .base import *
from .ldap import *
from .email import *

DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_USE_SSL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
