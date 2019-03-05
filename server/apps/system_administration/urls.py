from django.urls import path

from .views.system_settings_api import SystemSettingsAPI, ReadSystemSettings
from .views.log_entry_api import LogEntryView
from .views.content_type_value_help import ContentTypeValueHelp
from .views.announcement import AnnouncementCreate, AnnouncementDelete, AnnouncementUpdate, AnnouncementList

urlpatterns = [
    path(r'getSettings', ReadSystemSettings.as_view()),
    path(r'settings', SystemSettingsAPI.as_view()),
    path(r'logentries', LogEntryView.as_view()),
    path(r'content_types', ContentTypeValueHelp.as_view()),
    path(r'announcements', AnnouncementList.as_view()),
    path(r'announcement', AnnouncementCreate.as_view()),
    path(r'announcement/delete/<int:pk>', AnnouncementDelete.as_view()),
    path(r'announcement/<int:pk>', AnnouncementUpdate.as_view())
]
