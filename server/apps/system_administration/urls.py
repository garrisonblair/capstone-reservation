from django.urls import path

from .views.system_settings_api import SystemSettingsAPI
from .views.log_entry_api import LogEntryView

urlpatterns = [
    path(r'settings', SystemSettingsAPI.as_view()),
    path(r'logentries', LogEntryView.as_view())
]
