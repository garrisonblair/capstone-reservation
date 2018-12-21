from django.db import models


class SystemSettings(models.Model):

    variant = models.CharField(max_length=20, primary_key=True)

    is_webcalendar_backup_active = models.BooleanField(default=False)
    webcalendar_username = models.TextField(blank=True)
    webcalendar_password = models.TextField(blank=True)

    merge_adjacent_bookings = models.BooleanField(default=False)
    merge_threshold_minutes = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_settings():
        try:
            settings = SystemSettings.objects.get(variant="")
        except SystemSettings.DoesNotExist:
            settings = SystemSettings(variant="")
            settings.save()

        return settings
