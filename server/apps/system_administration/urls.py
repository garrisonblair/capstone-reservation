from django.urls import path

from .views.system_settings_api import SystemSettingsAPI
from .views.log_entry_api import LogEntryView
from .views.content_type_value_help import ContentTypeValueHelp

urlpatterns = [
    path(r'settings', SystemSettingsAPI.as_view()),
    path(r'logentries', LogEntryView.as_view()),
    path(r'content_types', ContentTypeValueHelp.as_view())
]
