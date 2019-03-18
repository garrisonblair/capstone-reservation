from celery import shared_task
from apps.notifications.models.BookingReminder import BookingReminder


@shared_task
def send_booking_reminders():
    BookingReminder.objects.send_reminders()
