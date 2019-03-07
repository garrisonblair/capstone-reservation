from __future__ import unicode_literals
import os
import dotenv

from celery import Celery

env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
if os.path.exists(env_file_path):
    dotenv.read_dotenv(env_file_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings.{}'.format(os.environ.get('DJANGO_ENV')))

app = Celery('proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
