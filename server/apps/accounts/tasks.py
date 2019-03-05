from celery import shared_task
from django.core import mail
from django.conf import settings


@shared_task
def send_email(subject, message, recipient_list):
    mail.send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
