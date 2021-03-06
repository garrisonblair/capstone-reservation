import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from apps.system_administration.views.system_settings_api import SystemSettingsAPI, ReadSystemSettings
from apps.system_administration.models.system_settings import SystemSettings


class TestSettingsAPI(TestCase):

    def setUp(self):
        self.user = User(username="admin")
        self.user.is_superuser = True
        self.user.save()

        self.factory = APIRequestFactory()

    def testGetSettings(self):

        settings = SystemSettings.get_settings()

        request = self.factory.get("/getSettings")
        force_authenticate(request, self.user)
        response = ReadSystemSettings().as_view()(request)

        response_data = response.data
        self.assertEqual(response.data["variant"], settings.variant)
        self.assertEqual(response.data["is_webcalendar_backup_active"], settings.is_webcalendar_backup_active)

        with self.assertRaises(KeyError):
            # read fields that should never be exposed through the UI to trigger KeyError
            response.data["webcalendar_username"]
            response.data["webcalendar_password"]

    @unittest.skip
    def testUpdateWebCalendarBackup(self):
        settings = SystemSettings.get_settings()
        updated_settings = {
                                 "is_webcalendar_backup_active": True,
                                 "webcalendar_username": "f_daigl",
                                 "webcalendar_password": "mySafePassword"
                             }
        request = self.factory.patch("/settings", updated_settings, format="json")
        force_authenticate(request, self.user)
        response = SystemSettingsAPI().as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        settings.refresh_from_db()
        self.assertEqual(settings.is_webcalendar_backup_active, updated_settings["is_webcalendar_backup_active"])
        self.assertEqual(settings.webcalendar_username, updated_settings["webcalendar_username"])
        self.assertEqual(settings.webcalendar_password, updated_settings["webcalendar_password"])
