from django.db import models
from django.apps import apps
from model_utils import FieldTracker


class SystemSettings(models.Model):

    variant = models.CharField(max_length=20, primary_key=True)
    is_webcalendar_backup_active = models.BooleanField(default=False)
    webcalendar_username = models.TextField()
    webcalendar_password = models.TextField()

    tracker = FieldTracker()

    @staticmethod
    def get_settings():
        try:
            settings = SystemSettings.objects.get(variant="")
        except SystemSettings.DoesNotExist:
            settings = SystemSettings(variant="")
            settings.save()

        return settings

    def save(self, *args, **kwargs):

        this = super(SystemSettings, self).save(*args, **kwargs)

        # Check if Webcalendar exporter needs to be registered/unregistered.
        if self.tracker.has_changed("is_webcalendar_backup_active"):
            booking_exporter_config = apps.get_app_config("booking_exporter")
            if self.is_webcalendar_backup_active:
                booking_exporter_config.register_web_calender_exporter()
            else:
                booking_exporter_config.unregister_web_calendar_exporter()

        return this
