from django.test import TestCase

from apps.accounts.models.User import User
from apps.booker_settings.models.PersonalSettings import PersonalSettings

from django.core.exceptions import ValidationError


class TestPersonalSettings(TestCase):
    def setUp(self):
        # Setup one booker
        self.booker = User.objects.create_user(username="booker",
                                               email="booker@email.com",
                                               password="booker")
        self.booker.save()

    def testPersonalSettingCreation(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#000000",
                                   campon_color="#000000",
                                   passed_booking_color="#000000")
        setting.save()
        self.assertEqual(setting, PersonalSettings.objects.get(booker=self.booker))
        self.assertEqual(PersonalSettings.objects.count(), 1)

    def testPersonalSettingCreateFailedWithBookingColor(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#",
                                   campon_color="#000000",
                                   passed_booking_color="#000000")

        with self.assertRaises(ValidationError) as ex:
            setting.save()

    def testPersonalSettingCreateFailedWithCamponColor(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#000000",
                                   campon_color="#",
                                   passed_booking_color="#000000")

        with self.assertRaises(ValidationError) as ex:
            setting.save()

    def testPersonalSettingCreateFailedWithCamponColor(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#000000",
                                   campon_color="#000000",
                                   passed_booking_color="#")

        with self.assertRaises(ValidationError) as ex:
            setting.save()
