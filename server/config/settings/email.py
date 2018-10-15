import os

# Email config
EMAIL_USE_SSL = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
ROOT_PROTOCOL = os.environ.get('ROOT_PROTOCOL')
ROOT_URL = os.environ.get('ROOT_URL')
