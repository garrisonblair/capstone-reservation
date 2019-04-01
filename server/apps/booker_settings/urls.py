from django.urls import path
from .views.email_settings import EmailSettings
from .views.email_settings_service import EmailSettingsService
from .views.personal_settings import PersonalSettingsCreateRetrieveUpdate
from .views.personal_settings_service import PersonalSettingsService

urlpatterns = [
    path(r'email_settings', EmailSettings.as_view()),
    path(r'email_settings_service', EmailSettingsService.as_view()),
    path(r'personal_settings', PersonalSettingsCreateRetrieveUpdate.as_view()),
    path(r'personal_settings_service', PersonalSettingsService.as_view()),
]
