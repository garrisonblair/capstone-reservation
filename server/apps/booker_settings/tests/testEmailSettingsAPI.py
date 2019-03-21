from django.test.testcases import TestCase
from django.contrib.auth.models import User

from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

from apps.booker_settings.models.EmailSettings import EmailSettings
from apps.booker_settings.views.email_settings import EmailSettings as EmailSettingsView


class EmailSettingsAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.booker = User.objects.create_user(username='john',
                                               email='jlennon@beatles.com',
                                               password='glass onion')
        self.booker.save()
        email_settings = EmailSettings(booker=self.booker)
        email_settings.save()

    def testGetEmailSettings(self):
        request = self.factory.get("/email_settings")
        force_authenticate(request, user=self.booker)
        response = EmailSettingsView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_email_settings = response.data
        self.assertEqual(True, "when_booking" in returned_email_settings)
        self.assertEqual(True, "when_invitation" in returned_email_settings)
        self.assertEqual(True, "booking_reminder" in returned_email_settings)
        self.assertEqual(True, "when_camp_on_booking" in returned_email_settings)
        self.assertEqual(True, "id" in returned_email_settings)
        self.assertEqual(True, "booker" in returned_email_settings)

    def testPostEmailSettingsSuccessful(self):
        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_invitation": False,
                                        "booking_reminder": False,
                                        "when_camp_on_booking": False
                                        }, format="json")
        force_authenticate(request, user=self.booker)
        response = EmailSettingsView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_email_settings = EmailSettings.objects.get(booker=self.booker)

        self.assertEqual(False, current_email_settings.when_booking)
        self.assertEqual(False, current_email_settings.when_invitation)
        self.assertEqual(False, current_email_settings.booking_reminder)
        self.assertEqual(False, current_email_settings.when_camp_on_booking)

    def testPostEmailSettingsFailure(self):
        request = self.factory.post('email_settings',{
                                        "when_booking":1,
                                        "when_invitation": False,
                                        "booking_reminder": False,
                                        "when_camp_on_booking": False
                                        }, format="json")
        force_authenticate(request, user=self.booker)
        response = EmailSettingsView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_invitation": 2,
                                        "booking_reminder": False,
                                        "when_camp_on_booking": False
                                        }, format="json")
        force_authenticate(request, user=self.booker)
        response = EmailSettingsView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_invitation": False,
                                        "booking_reminder": 1,
                                        "when_camp_on_booking": False
                                        }, format="json")
        force_authenticate(request, user=self.booker)
        response = EmailSettingsView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post('email_settings',{
                                        "when_booking":False,
                                        "when_invitation": False,
                                        "booking_reminder": False,
                                        "when_camp_on_booking": 2
                                        }, format="json")
        force_authenticate(request, user=self.booker)
        response = EmailSettingsView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
