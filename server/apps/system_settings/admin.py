from django.contrib import admin
from .models.system_settings import SystemSettings


class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('webcalendar_username', 'webcalendar_password', 'is_webcalendar_backup_active', 'variant')

admin.site.register(SystemSettings, SystemSettingsAdmin)
