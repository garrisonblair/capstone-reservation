from django.urls import path
from .views.email_settings import EmailSettings
from .views.email_settings_service import EmailSettingsService
from .views.personal_settings import PersonalSettingsCreate
from .views.personal_settings import PersonalSettingsUpdate
from .views.personal_settings import PersonalSettingsList
from .views.personal_settings_service import PersonalSettingsService

urlpatterns = [
    path(r'email_settings', EmailSettings.as_view()),
    path(r'email_settings_service', EmailSettingsService.as_view()),
    path(r'personal_settings', PersonalSettingsCreate.as_view()),
    path(r'personal_settings/<int:pk>', PersonalSettingsUpdate.as_view()),
    path(r'personal_settings_list/<int:pk>', PersonalSettingsList.as_view()),
    path(r'personal_settings_service', PersonalSettingsService.as_view()),
]
