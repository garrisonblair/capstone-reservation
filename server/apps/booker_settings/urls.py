from django.urls import path
from .views.email_settings import EmailSettings

urlpatterns = [
    path(r'email_settings', EmailSettings.as_view())
]
