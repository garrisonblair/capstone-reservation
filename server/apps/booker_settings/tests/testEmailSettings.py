from django.test import TestCase
from apps.accounts.models.User import User
from apps.booker_settings.models.EmailSettings import EmailSettings
from django.core.exceptions import ValidationError


class TestEmailSettings(TestCase):
    def setUp(self):
        self.booker1 = User.objects.create_user(username="f_daigl",
                                                email="fred@email.com",
                                                password="safe_password")  # type: User
        self.booker2 = User.objects.create_user(username="user_name",
                                                email="fred2@email.com",
                                                password="safe_password2")  # type: User
        self.booker1.save()
        self.booker2.save()

    def testEmailSettingsCreation(self):
        table_length = len(EmailSettings.objects.all())
        email_settings = EmailSettings(booker=self.booker1)
        email_settings.save()
        self.assertEqual(True, email_settings.when_booking)
        self.assertEqual(True, email_settings.when_invitation)
        self.assertEqual(True, email_settings.booking_reminder)
        self.assertEqual(True, email_settings.when_camp_on_booking)
        self.assertEqual(table_length + 1, len(EmailSettings.objects.all()))

    def testEmailSettingsWrongTypeUpdate(self):
        email_settings1 = EmailSettings(booker=self.booker1)
        email_settings1.save()

        email_settings1.when_booking = False
        data = {
            "when_booking": False,
            "when_invitation": False,
            "booking_reminder": False,
            "when_camp_on_booking": False,
        }
        email_settings1.update(data)

        email_settings2 = EmailSettings(booker=self.booker2)
        email_settings2.save()

        data['when_booking'] = 1
        with self.assertRaises(ValidationError):
            email_settings2.update(data)

        data['when_invitation'] = 1
        with self.assertRaises(ValidationError):
            email_settings2.update(data)

        data['booking_reminder'] = 1
        with self.assertRaises(ValidationError):
            email_settings2.update(data)

        data['when_camp_on_booking'] = 1
        with self.assertRaises(ValidationError):
            email_settings2.update(data)
