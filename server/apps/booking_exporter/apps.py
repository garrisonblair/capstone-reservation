import threading

from django.apps import AppConfig


class BookingExporterConfig(AppConfig):
    name = 'apps.booking_exporter'

    def __init__(self, arg1, arg2):
        super(BookingExporterConfig, self).__init__(arg1, arg2)
        self.web_calendar_exporter = None
        self.importer_thread = None  # type: threading.Timer

    def ready(self):
        from apps.system_administration.models.system_settings import SystemSettings

        try:
            settings = SystemSettings.get_settings()

            if settings.is_webcalendar_backup_active:
                self.register_web_calender_exporter()

        except Exception:  # Fails during migrations
            pass

        self.start_importing_ics_bookings()

    def register_web_calender_exporter(self):
        from .WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter
        from apps.booking.models.Booking import Booking
        if self.web_calendar_exporter is None:
            self.web_calendar_exporter = WEBCalendarExporter()

        Booking().register(self.web_calendar_exporter)

    def unregister_web_calendar_exporter(self):
        from apps.booking.models.Booking import Booking
        if self.web_calendar_exporter is not None:
            Booking().unregister(self.web_calendar_exporter)

    def start_importing_ics_bookings(self):
        from .GmailImporter.GmailICSImporter import GmailICSImporter

        self.importer_thread = threading.Timer(10, self.start_importing_ics_bookings)
        self.importer_thread.start()

        importer = GmailICSImporter()
        importer.import_unprocessed_bookings()

    def stop_importing_ics_bookings(self):
        self.importer_thread.stop()
