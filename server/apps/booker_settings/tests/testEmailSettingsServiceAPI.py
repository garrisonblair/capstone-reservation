from django.test.testcases import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework import status

from apps.util.Jwt import getUserFromToken, generateToken
from apps.booker_settings.models.EmailSettings import EmailSettings
from apps.booker_settings.views.email_settings_service import EmailSettingsService as EmailSettingsServiceView


class EmailSettingsAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.booker = User.objects.create_user(username='john',
                                               email='jlennon@beatles.com',
                                               password='glass onion')
        self.booker.save()
        email_settings = EmailSettings(booker=self.booker)
        email_settings.save()
        self.token = generateToken(self.booker)


    def testGetEmailSettingsSuccesful(self):
        token = generateToken(self.booker)
        request = self.factory.get('/email_settings_service', HTTP_AUTHORIZATION=token)
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_email_settings = response.data
        self.assertEqual(True, "when_booking" in returned_email_settings)
        self.assertEqual(True, "when_delete_booking" in returned_email_settings)
        self.assertEqual(True, "when_delete_recurring_booking" in returned_email_settings)
        self.assertEqual(True, "when_camp_on_booking" in returned_email_settings)
        self.assertEqual(True, "id" in returned_email_settings)
        self.assertEqual(True, "booker" in returned_email_settings)

    def testGetEmailSettingsWrongToken(self):
        request = self.factory.get('/email_settings_service', HTTP_AUTHORIZATION=self.token+'3124')
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testGetEmailSettingsNoToken(self):
        request = self.factory.get('/email_settings_service')
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testPostEmailSettingsNoToken(self):
        request = self.factory.post('/email_settings_service')
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testPostEmailSettingsWrongToken(self):
        request = self.factory.post('/email_settings_service', HTTP_AUTHORIZATION=self.token+'3124')
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testPostEmailSettingsSucessful(self):
        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_delete_booking": False,
                                        "when_delete_recurring_booking": False,
                                        "when_camp_on_booking": False
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        current_email_settings = EmailSettings.objects.get(booker=self.booker)

        self.assertEqual(False, current_email_settings.when_booking)
        self.assertEqual(False, current_email_settings.when_delete_booking)
        self.assertEqual(False, current_email_settings.when_delete_recurring_booking)
        self.assertEqual(False, current_email_settings.when_camp_on_booking)

    def testPostEmailSettingsWrongData(self):
        request = self.factory.post('email_settings',{
                                        "when_booking":1,
                                        "when_delete_booking": False,
                                        "when_delete_recurring_booking": False,
                                        "when_camp_on_booking": False
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_delete_booking": 1,
                                        "when_delete_recurring_booking": False,
                                        "when_camp_on_booking": False
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_delete_booking": False,
                                        "when_delete_recurring_booking": 1,
                                        "when_camp_on_booking": False
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_delete_booking": False,
                                        "when_delete_recurring_booking": False,
                                        "when_camp_on_booking": 1
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = EmailSettingsServiceView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


