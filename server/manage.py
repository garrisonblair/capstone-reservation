import os
import sys
import dotenv

if __name__ == '__main__':
    # Read .env file
    env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_file_path):
        dotenv.read_dotenv(env_file_path)
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
