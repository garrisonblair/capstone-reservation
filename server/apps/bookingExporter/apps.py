from django.apps import AppConfig


class BookingExporterConfig(AppConfig):
    name = 'apps.bookingExporter'

    def __init__(self, arg1, arg2):
        super(BookingExporterConfig, self).__init__(arg1, arg2)
        self.web_calendar_exporter = None

    def ready(self):

        self.register_web_calender_exporter()
        # TODO: Check system settings
        pass

    def register_web_calender_exporter(self):
        from .WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter
        from apps.booking.models.Booking import Booking
        if self.web_calendar_exporter is None:
            self.web_calendar_exporter = WEBCalendarExporter()

        Booking().register(self.web_calendar_exporter)
