from django.test import TestCase
from apps.accounts.models.User import User
from apps.booker_settings.models.EmailSettings import EmailSettings


class TestEmailSettings(TestCase):
    def setUp(self):
        self.booker = User.objects.create_user(username="f_daigl",
                                               email="fred@email.com",
                                               password="safe_password")  # type: User
        self.booker.save()

    def testEmailSettingsCreation(self):
        tableLength = len(EmailSettings.objects.all())
        email_settings = EmailSettings(booker=self.booker)
        email_settings.save()
        self.assertEqual(True,email_settings.when_booking)
        self.assertEqual(True,email_settings.when_recurring_booking)
        self.assertEqual(True,email_settings.when_delete_booking)
        self.assertEqual(True,email_settings.when_delete_recurring_booking)
        self.assertEqual(True,email_settings.when_camp_on_booking)
        self.assertEqual(tableLength + 1, len(EmailSettings.objects.all()))

