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

    def testPersonalSettingDefaultCreation(self):
        setting = PersonalSettings(booker=self.booker)
        setting.save()

        real_setting = PersonalSettings.objects.get(booker=self.booker)
        self.assertEqual(setting, real_setting)
        self.assertEqual(real_setting.schedule_vertical, True)
        self.assertEqual(real_setting.booking_color, "#1F5465")
        self.assertEqual(real_setting.campon_color, "#82220E")
        self.assertEqual(real_setting.passed_booking_color, "#7F7F7F")

    def testPersonalSettingPartialDefaultCreation(self):
        setting = PersonalSettings(booker=self.booker,
                                   booking_color="#000000")
        setting.save()

        real_setting = PersonalSettings.objects.get(booker=self.booker)
        self.assertEqual(setting, real_setting)
        self.assertEqual(real_setting.schedule_vertical, True)
        self.assertEqual(real_setting.booking_color, "#000000")
        self.assertEqual(real_setting.campon_color, "#82220E")
        self.assertEqual(real_setting.passed_booking_color, "#7F7F7F")

    def testPersonalSettingCreateFailedWithBookingColor(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#",
                                   campon_color="#000000",
                                   passed_booking_color="#000000")

        with self.assertRaises(ValidationError):
            setting.save()

    def testPersonalSettingCreateFailedWithCamponColor(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#000000",
                                   campon_color="#",
                                   passed_booking_color="#000000")

        with self.assertRaises(ValidationError):
            setting.save()

    def testPersonalSettingCreateFailedWithCamponColor(self):
        setting = PersonalSettings(booker=self.booker,
                                   schedule_vertical=False,
                                   booking_color="#000000",
                                   campon_color="#000000",
                                   passed_booking_color="#")

        with self.assertRaises(ValidationError):
            setting.save()
