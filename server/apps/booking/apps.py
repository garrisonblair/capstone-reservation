import threading
import os
from django.apps import AppConfig
from apps.util import Logging

logger = Logging.get_logger()


class BookingConfig(AppConfig):
    name = 'apps.booking'

    expired_booking_checker_thread = None

    def __init__(self, arg1):
        super(BookingConfig, self).__init__(arg1)
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
        from apps.system_administration.models.system_settings import SystemSettings

        settings = SystemSettings.get_settings()

        expired_booking_checker_thread = threading.Timer(settings.check_expired_booking_frequency_seconds,
                                                         self.start_checking_for_expired_bookings_active)
        expired_booking_checker_thread.start()
        self.expired_booking_checker_thread = expired_booking_checker_thread

    def stop_checking_for_expired_bookings(self):
        if self.expired_booking_checker_thread:
            self.expired_booking_checker_thread.cancel()
            self.expired_booking_checker_thread = None
