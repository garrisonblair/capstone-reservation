from django.db import models
from django.apps import apps
from model_utils import FieldTracker
from datetime import timedelta


class SystemSettings(models.Model):

    variant = models.CharField(max_length=20, primary_key=True)

    is_webcalendar_backup_active = models.BooleanField(default=False)
    webcalendar_username = models.TextField(blank=True)
    webcalendar_password = models.TextField(blank=True)

    is_webcalendar_synchronization_active = models.BooleanField(default=False)
    import_frequency_seconds = models.PositiveIntegerField(default=30)

    merge_adjacent_bookings = models.BooleanField(default=False)
    merge_threshold_minutes = models.PositiveIntegerField(default=0)

    booking_edit_lock_timeout = models.DurationField(default=timedelta())

    group_can_invite_after_privilege_set = models.BooleanField(default=True)

    # Setting to toggle the checking of expired bookings, the duration at which to check for them, and the time that
    # the admin sets at which a booking expires after reaching (in minutes)
    check_for_expired_bookings_active = models.BooleanField(default=False)
    campons_refutable = models.BooleanField(default=False)
    check_for_expired_bookings_frequency_seconds = models.PositiveIntegerField(default=30)
    booking_time_to_expire_minutes = models.PositiveIntegerField(default=30)
    manual_booking_confirmation = models.BooleanField(default=False)

    tracker = FieldTracker()

    @staticmethod
    def get_settings():
        try:
            settings = SystemSettings.objects.get(variant="default")
        except SystemSettings.DoesNotExist:
            settings = SystemSettings(variant="default")
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

        if self.tracker.has_changed("is_webcalendar_synchronization_active"):
            booking_exporter_config = apps.get_app_config("booking_exporter")

            if self.is_webcalendar_synchronization_active:
                booking_exporter_config.start_importing_ics_bookings()
            else:
                booking_exporter_config.stop_importing_ics_bookings()

        return this

    def __str__(self):
        return "System Setting"
