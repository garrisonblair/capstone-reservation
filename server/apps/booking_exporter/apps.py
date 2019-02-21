import os
from django.apps import AppConfig
from apps.util import Logging

logger = Logging.get_logger()


class BookingExporterConfig(AppConfig):
    name = 'apps.booking_exporter'
    gmail_import_periodic_task_name = "gmail_ics_importing"

    def __init__(self, arg1, arg2):
        super(BookingExporterConfig, self).__init__(arg1, arg2)
        self.web_calendar_exporter = None

        print(os.path.dirname(os.path.abspath(__file__)))

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
        from apps.system_administration.models.system_settings import SystemSettings
        from django_celery_beat.schedulers import PeriodicTask, IntervalSchedule

        settings = SystemSettings.get_settings()
        schedule = IntervalSchedule(every=settings.import_frequency_seconds,
                                    period=IntervalSchedule.SECONDS)
        schedule.save()

        ics_import_task = PeriodicTask(name=self.gmail_import_periodic_task_name,
                                       task='apps.booking_exporter.tasks.importGmailICSFiles',
                                       interval=schedule)
        try:
            ics_import_task.save()
        except Exception:  # fails if task already exists
            pass

    def stop_importing_ics_bookings(self):
        from django_celery_beat.schedulers import PeriodicTask, IntervalSchedule
        try:
            task = PeriodicTask.objects.get(name=self.gmail_import_periodic_task_name)
            task.delete()
        except Exception:
            logger.warn("Gmail importing task could not be deleted")
