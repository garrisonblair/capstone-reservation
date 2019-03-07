from celery import shared_task
from datetime import datetime, timedelta, date

from .models.Booking import Booking
from apps.system_administration.models.system_settings import SystemSettings


@shared_task
def check_expired_bookings():
    current_date = datetime.now()
    bookings_to_check = Booking.objects.filter(date=current_date, confirmed=False)
    current_time = current_date.time()

    settings = SystemSettings.get_settings()

    # Ensure that current time has passed expiration time
    for booking in bookings_to_check:
        if booking.expiration_base:
            expiration = booking.get_expiration()
            if expiration < current_time:
                booking.delete_booking()
