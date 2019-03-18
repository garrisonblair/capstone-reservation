from django.urls import path
from .views.email_settings import EmailSettings
from .views.email_settings_service import EmailSettingsService

urlpatterns = [
    path(r'email_settings', EmailSettings.as_view()),
    path(r'email_settings_service', EmailSettingsService.as_view())
]
