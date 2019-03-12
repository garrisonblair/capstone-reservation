import os
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'

    booking_reminder_task_name = 'booking_reminder_task'

    def ready(self):
        from apps.system_administration.models.system_settings import SystemSettings
        if os.environ.get('RUN_MAIN', None) == 'true':
            try:
                settings = SystemSettings.get_settings()

                if settings.booking_reminders_active:
                    self.start_booking_reminder_task()

            except Exception:
                pass

    def start_booking_reminder_task(self):
        from django_celery_beat.schedulers import PeriodicTask, IntervalSchedule

        schedule = IntervalSchedule(every=5,
                                    period=IntervalSchedule.MINUTES)

        schedule.save()

        booking_reminder_task = PeriodicTask(name=self.booking_reminder_task_name,
                                             task='apps.notifications.tasks.send_booking_reminders',
                                             interval=schedule)
        try:
            booking_reminder_task.save()
        except Exception:
            pass

    def stop_booking_reminder_task(self):
        from django_celery_beat.schedulers import PeriodicTask

        task = PeriodicTask.objects.get(name=self.booking_reminder_task_name)
        task.delete()
