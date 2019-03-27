from django.test.testcases import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework import status

from apps.util.Jwt import generate_token
from apps.booker_settings.models.PersonalSettings import PersonalSettings
from apps.booker_settings.views.personal_settings_service import PersonalSettingsService


class PersonalSettingsAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.booker = User.objects.create_user(username='booker',
                                               email='booker@booker.com',
                                               password='booker')
        self.booker.save()
        personal_settings = PersonalSettings(booker=self.booker)
        personal_settings.save()
        self.token = generate_token(self.booker)

    def testGetPersonalSettingsSuccessful(self):
        token = generate_token(self.booker)
        request = self.factory.get('/personal_settings_service', HTTP_AUTHORIZATION=token)
        response = PersonalSettingsService.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_settings = response.data
        self.assertEqual(real_settings['schedule_vertical'], True)
        self.assertEqual(real_settings['booking_color'], "#1F5465")
        self.assertEqual(real_settings['campon_color'], "#82220E")
        self.assertEqual(real_settings['passed_booking_color'], "#7F7F7F")

    def testGetPersonalSettingsWrongToken(self):
        request = self.factory.get('/personal_settings_service', HTTP_AUTHORIZATION=self.token+'9999')
        response = PersonalSettingsService.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testGetPersonalSettingsNoToken(self):
        request = self.factory.get('/personal_settings_service')
        response = PersonalSettingsService.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testPostPersonalSettingsNoToken(self):
        request = self.factory.post('/personal_settings_service')
        response = PersonalSettingsService.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testPostPersonalSettingsWrongToken(self):
        request = self.factory.post('/personal_settings_service', HTTP_AUTHORIZATION=self.token+'9999')
        response = PersonalSettingsService.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testPostPersonalSettingsSuccessful(self):
        request = self.factory.post('personal_settings_service', {
                                        "schedule_vertical": False,
                                        "booking_color": "#000000",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = PersonalSettingsService.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        real_settings = PersonalSettings.objects.get(booker=self.booker)
        self.assertEqual(real_settings.schedule_vertical, False)
        self.assertEqual(real_settings.booking_color, "#000000")
        self.assertEqual(real_settings.campon_color, "#000000")
        self.assertEqual(real_settings.passed_booking_color, "#000000")

    def testPostPersonalSettingsWrongData(self):
        request = self.factory.post('personal_settings_service', {
                                        "schedule_vertical": False,
                                        "booking_color": "#",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                        }, format="json", HTTP_AUTHORIZATION=self.token)
        response = PersonalSettingsService.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
