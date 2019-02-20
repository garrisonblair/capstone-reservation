import threading
import os
from datetime import datetime
from django.apps import AppConfig
from apps.util import Logging

logger = Logging.get_logger()


class BookingConfig(AppConfig):
    name = 'apps.booking'

    expired_booking_checker_thread = None

    def __init__(self, arg1, arg2):
        super(BookingConfig, self).__init__(arg1, arg2)
        self.expired_booking_checker_thread = None

    def ready(self):
        from apps.system_administration.models.system_settings import SystemSettings
        if os.environ.get('RUN_MAIN', None) == 'true':
            try:
                settings = SystemSettings.get_settings()

                if settings.check_for_expired_bookings_active:
                    self.start_checking_for_expired_bookings()
                    pass

            except Exception:
                pass

    def start_checking_for_expired_bookings(self):
        from apps.booking.models.Booking import Booking
        from apps.system_administration.models.system_settings import SystemSettings

        settings = SystemSettings.get_settings()

        expired_booking_checker_thread = threading.Timer(settings.check_expired_booking_frequency_seconds,
                                                         self.start_checking_for_expired_bookings_active)
        expired_booking_checker_thread.start()
        self.expired_booking_checker_thread = expired_booking_checker_thread

        current_date = datetime.now()
        bookings_to_check = Booking.objects.filter(date=current_date, confirmed=False)
        current_time = current_date.time()

        for booking in bookings_to_check:
            if booking.expiration < current_time:
                booking.delete_booking()

    def stop_checking_for_expired_bookings(self):
        if self.expired_booking_checker_thread:
            self.expired_booking_checker_thread.cancel()
            self.expired_booking_checker_thread = None
