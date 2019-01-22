import os
import dotenv
import sys
import site
from django.core.wsgi import get_wsgi_application

# Read .env file
env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
if os.path.exists(env_file_path):
    dotenv.read_dotenv(env_file_path)

VIRTUAL_ENV_DIR = "/home/webcal/Desktop/venv/CapstoneReservation"  # Root path of the virtual environment directory
PROJECT_DIR = "/home/webcal/Desktop/GitHub/CapstoneReservation/server"  # Root path of the project directory
CONFIG_DIR = "/home/webcal/Desktop/GitHub/CapstoneReservation/server/config"  # Root path of the project directory
PYTHON_VERSION = '3.6'  # Python version in the virtual environment directory

ALLDIRS = [
    PROJECT_DIR,
    CONFIG_DIR,
    "{}/lib/python{}/site-packages".format(VIRTUAL_ENV_DIR, PYTHON_VERSION)
]


def update_sys_path():

    # Remember original sys.path.
    prev_sys_path = list(sys.path)

    # Add each new site-packages directory.
    for directory in ALLDIRS:
        site.addsitedir(directory)

    # Reorder sys.path so new directories at the front.
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    new_sys_path.append(CONFIG_DIR)
    sys.path[:0] = new_sys_path


update_sys_path()

# Activate virtual environment
activate_env = "{}/bin/activate_this.py".format(VIRTUAL_ENV_DIR)

with open(activate_env) as file:
    exec(file.read(), dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings.{}'.format(os.environ.get('DJANGO_ENV')))
application = get_wsgi_application()
