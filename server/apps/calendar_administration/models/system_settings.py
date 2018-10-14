from django.db import models


class SystemSettings(models.Model):
    variant = models.CharField(max_length=20, primary_key=True)
    is_webcalendar_backup_active = models.BooleanField(default=False)
    webcalendar_username = models.TextField()
    webcalendar_username = models.TextField()
