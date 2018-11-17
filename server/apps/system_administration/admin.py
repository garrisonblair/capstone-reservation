from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models.system_settings import SystemSettings

admin.site.register(SystemSettings)
admin.site.register(LogEntry)
