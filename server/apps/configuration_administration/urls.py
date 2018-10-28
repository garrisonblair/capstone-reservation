from django.urls import path

from .views.system_settings_api import SystemSettingsAPI

urlpatterns = [
    path(r'settings', SystemSettingsAPI.as_view())
]
