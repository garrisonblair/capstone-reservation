from apps.rooms.models.Room import Room

from django.test.testcases import TestCase
from django.contrib.auth.models import User

from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

from apps.booker_settings.models.PersonalSettings import PersonalSettings
from apps.booker_settings.views.email_settings_service import EmailSettingsService
from apps.booker_settings.views.personal_settings import PersonalSettingsCreate
from apps.booker_settings.views.personal_settings import PersonalSettingsRetrieveUpdateDestroy


class PersonalSettingsAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.booker = User.objects.create_user(username='booker',
                                               email='booker@booker.com',
                                               password='booker')
        self.booker.save()

        self.admin = User.objects.create_user(username="admin",
                                              is_superuser=True)

        self.admin.save()

    def testCreateDefaultPersonalSettingsSuccessful(self):

        request = self.factory.post("/personal_settings",
                                    {
                                        "booker": self.booker.id
                                    },
                                    format="json")

        force_authenticate(request, user=self.admin)
        response = PersonalSettingsCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.schedule_vertical, True)
        self.assertEqual(real_settings.booking_color, "#1F5465")
        self.assertEqual(real_settings.campon_color, "#82220E")
        self.assertEqual(real_settings.passed_booking_color, "#7F7F7F")

    def testCreatePartialDefaultPersonalSettingsSuccessful(self):

        request = self.factory.post("/personal_settings",
                                    {
                                        "booker": self.booker.id,
                                        "campon_color": "#000000"
                                    },
                                    format="json")

        force_authenticate(request, user=self.admin)
        response = PersonalSettingsCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        real_settings = PersonalSettings.objects.last()
        self.assertEqual(real_settings.schedule_vertical, True)
        self.assertEqual(real_settings.booking_color, "#1F5465")
        self.assertEqual(real_settings.campon_color, "#000000")
        self.assertEqual(real_settings.passed_booking_color, "#7F7F7F")
