import os
import dotenv

from django.core.wsgi import get_wsgi_application

# Read .env file
env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
if os.path.exists(env_file_path):
    dotenv.read_dotenv(env_file_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings.{}'.format(os.environ.get('DJANGO_ENV')))

application = get_wsgi_application()
