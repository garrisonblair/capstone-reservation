from django.test.testcases import TestCase
from django.contrib.auth.models import User

from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

from apps.booker_settings.models.PersonalSettings import PersonalSettings
from apps.booker_settings.views.personal_settings import PersonalSettingsCreateRetrieveUpdate


class PersonalSettingsAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.booker = User.objects.create_user(username='booker',
                                               email='booker@booker.com',
                                               password='booker')
        self.booker.save()

        self.booker2 = User.objects.create_user(username='booker2',
                                                email='booker2@booker.com',
                                                password='booker2')
        self.booker2.save()

    def testCreateDefaultPersonalSettingsSuccessful(self):

        request = self.factory.get("/personal_settings")

        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.booking_color, "#1F5465")
        self.assertEqual(real_settings.campon_color, "#82220E")
        self.assertEqual(real_settings.passed_booking_color, "#7F7F7F")

    def testCreatePersonalSettingsFailedWithBookingColor(self):

        request = self.factory.post("/personal_settings",
                                    {
                                        "booker": self.booker.id,
                                        "booking_color": "#"
                                    },
                                    format="json")

        force_authenticate(request, user=self.booker)

        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(PersonalSettings.objects.count(), 0)

    def testCreatePersonalSettingsFailedWithCamponColor(self):

        request = self.factory.post("/personal_settings",
                                    {
                                        "booker": self.booker.id,
                                        "campon_color": "#"
                                    },
                                    format="json")

        force_authenticate(request, user=self.booker)

        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(PersonalSettings.objects.count(), 0)

    def testCreatePersonalSettingsFailedWithPassedBookingColor(self):

        request = self.factory.post("/personal_settings",
                                    {
                                        "booker": self.booker.id,
                                        "passed_booking_color": "#"
                                    },
                                    format="json")

        force_authenticate(request, user=self.booker)

        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(PersonalSettings.objects.count(), 0)

    def testCreatePersonalSettingsFailedWithNoBoooker(self):

        request = self.factory.post("/personal_settings",
                                    {
                                        "booker": self.booker.id,
                                        "passed_booking_color": "#"
                                    },
                                    format="json")
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PersonalSettings.objects.count(), 0)

    def testUpdatePersonalSettingsSuccessful(self):

        setting = PersonalSettings(booker=self.booker)
        setting.save()

        request = self.factory.post("/personal_settings", {
                                        "booking_color": "#000000",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(PersonalSettings.objects.count(), 1)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.booking_color, "#000000")
        self.assertEqual(real_settings.campon_color, "#000000")
        self.assertEqual(real_settings.passed_booking_color, "#000000")

    def testUpdatePersonalSettingsNotChangingOriginal(self):

        setting = PersonalSettings(booker=self.booker)
        setting.save()

        request = self.factory.post("/personal_settings", {
                                        "booking_color": "#000000",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(PersonalSettings.objects.count(), 1)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.booking_color, "#000000")
        self.assertEqual(real_settings.campon_color, "#000000")
        self.assertEqual(real_settings.passed_booking_color, "#000000")

        request = self.factory.post("/personal_settings", {
                                        "booking_color": "#FFFFFF"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PersonalSettings.objects.count(), 1)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.booking_color, "#FFFFFF")
        self.assertEqual(real_settings.campon_color, "#000000")
        self.assertEqual(real_settings.passed_booking_color, "#000000")

    def testUpdatePersonalSettingsWithBookerNotFound(self):

        setting = PersonalSettings(booker=self.booker)
        setting.save()

        request = self.factory.post("/personal_settings", {
                                        "booking_color": "#000000",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker2)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testUpdatePersonalSettingsBookerStaysTheSame(self):

        setting = PersonalSettings(booker=self.booker)
        setting.save()

        request = self.factory.post("/personal_settings", {
                                        "booker": self.booker2.id,  # booker2 id instead of booker
                                        "booking_color": "#000000",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.booker.id, 1)  # booker id still 1
        self.assertEqual(real_settings.booking_color, "#000000")
        self.assertEqual(real_settings.campon_color, "#000000")
        self.assertEqual(real_settings.passed_booking_color, "#000000")

    def testUpdatePersonalSettingsWithBookerNotFound(self):

        request = self.factory.post("/personal_settings", {
                                        "booking_color": "#000000",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testUpdatePersonalSettingsWithInvalidColorCode(self):

        setting = PersonalSettings(booker=self.booker)
        setting.save()

        request = self.factory.post("/personal_settings", {
                                        "booking_color": "#",
                                        "campon_color": "#000000",
                                        "passed_booking_color": "#000000"
                                    },
                                    format="json")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testGetPersonalSettingsByTheSameBooker(self):

        setting = PersonalSettings(booker=self.booker)
        setting.save()

        request = self.factory.get("/personal_settings_list")
        force_authenticate(request, user=self.booker)
        response = PersonalSettingsCreateRetrieveUpdate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        real_settings = response.data
        self.assertEqual(real_settings['booking_color'], "#1F5465")
        self.assertEqual(real_settings['campon_color'], "#82220E")
        self.assertEqual(real_settings['passed_booking_color'], "#7F7F7F")
