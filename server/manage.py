import os
import sys
import dotenv

if __name__ == '__main__':
    # Read .env file
    dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings.{}'.format(os.environ.get('DJANGO_ENV')))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
