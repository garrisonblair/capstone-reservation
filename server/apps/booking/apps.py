import threading
import os
from datetime import datetime
from django.apps import AppConfig
from apps.util import Logging

logger = Logging.get_logger()


class BookingConfig(AppConfig):
    name = 'apps.booking'

    expired_booking_checker_task_name = "check_expired_bookings_task"

    expired_booking_checker_thread = None

    def __init__(self, arg1, arg2):
        super(BookingConfig, self).__init__(arg1, arg2)
        self.expired_booking_checker_thread = None

    def ready(self):
        from apps.system_administration.models.system_settings import SystemSettings
        from apps.booking import tasks
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
        from django_celery_beat.schedulers import PeriodicTask, IntervalSchedule

        settings = SystemSettings.get_settings()

        interval = IntervalSchedule(every=settings.check_for_expired_bookings_frequency_seconds,
                                    period=IntervalSchedule.SECONDS)

        interval.save()

        task = PeriodicTask(name=self.expired_booking_checker_task_name,
                            task="apps.booking.tasks.check_expired_bookings",
                            interval=interval)

        try:
            task.save()
        except Exception as e:
            print(e)

    def stop_checking_for_expired_bookings(self):
        from django_celery_beat.schedulers import PeriodicTask
        try:
            task = PeriodicTask.objects.get(name=self.expired_booking_checker_task_name)
            task.delete()
        except Exception:
            pass
