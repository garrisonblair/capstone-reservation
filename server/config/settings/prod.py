from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

PROJECT_APPS = [
    'apps.accounts.apps.AccountsConfig',
    'apps.rooms.apps.RoomsConfig',
    'apps.booking.apps.BookingConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
