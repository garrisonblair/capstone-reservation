from celery import shared_task
from django.core import mail
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def send_email(subject, message, recipient_list, ics_data=None):
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list
    )
    if ics_data is not None:
        email.attach('my_booking.ics', ics_data)
    email.send()
