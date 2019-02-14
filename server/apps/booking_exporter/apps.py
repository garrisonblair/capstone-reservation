import threading
import os
from django.apps import AppConfig
from apps.util import Logging

logger = Logging.get_logger()


class BookingExporterConfig(AppConfig):
    name = 'apps.booking_exporter'

    importer_thread = None
    expired_booking_checker_thread = None

    def __init__(self, arg1, arg2):
        super(BookingExporterConfig, self).__init__(arg1, arg2)
        self.web_calendar_exporter = None
        self.importer_thread = None

    def ready(self):
        from apps.system_administration.models.system_settings import SystemSettings
        if os.environ.get('RUN_MAIN', None) == 'true':
            try:
                settings = SystemSettings.get_settings()

                if settings.is_webcalendar_backup_active:
                    self.register_web_calender_exporter()

                # check that this is main thread, needed in dev environment because 2 apps are loaded
                if settings.is_webcalendar_synchronization_active:
                    self.start_importing_ics_bookings()

            except Exception:  # Fails during migrations
                pass

    def register_web_calender_exporter(self):
        from .WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter
        from apps.booking.models.Booking import Booking
        from apps.booking.models.CampOn import CampOn
        if self.web_calendar_exporter is None:
            self.web_calendar_exporter = WEBCalendarExporter()

        Booking().register(self.web_calendar_exporter)
        CampOn().register(self.web_calendar_exporter)

        logger.info("Webcalendar exporting turned on")

    def unregister_web_calendar_exporter(self):
        from apps.booking.models.Booking import Booking
        from apps.booking.models.CampOn import CampOn
        if self.web_calendar_exporter is not None:
            Booking().unregister(self.web_calendar_exporter)
            CampOn().unregister(self.web_calendar_exporter)

            logger.info("Webcalendar exporting turned off")

    def start_importing_ics_bookings(self):
        from .GmailImporter.GmailICSImporter import GmailICSImporter
        from apps.system_administration.models.system_settings import SystemSettings

        settings = SystemSettings.get_settings()

        importer_thread = threading.Timer(settings.import_frequency_seconds, self.start_importing_ics_bookings)
        importer_thread.start()
        self.importer_thread = importer_thread

        importer = GmailICSImporter()
        importer.import_unprocessed_bookings()

    def stop_importing_ics_bookings(self):
        if self.importer_thread:
            self.importer_thread.cancel()
            self.importer_thread = None

    def start_checking_for_expired_bookings(self):
        from .GmailImporter.GmailICSImporter import GmailICSImporter
        from apps.system_administration.models.system_settings import SystemSettings

        settings = SystemSettings.get_settings()

        expired_booking_checker_thread = threading.Timer(settings.check_expired_booking_frequency_seconds,
                                                         self.start_checking_expired_bookings)
        expired_booking_checker_thread.start()
        self.expired_booking_checker_thread = expired_booking_checker_thread

    def stop_checking_for_expired_bookings(self):
        if self.expired_booking_checker_thread:
            self.expired_booking_checker_thread.cancel()
            self.expired_booking_checker_thread = None
