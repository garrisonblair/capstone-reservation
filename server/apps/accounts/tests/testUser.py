from django.test import TestCase
from django.core import mail
import unittest

from apps.accounts.models.User import User


class TestUser(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='f_daigl',
                                             email='first_email@email.com')
        self.user.save()

    @unittest.skip
    def testSendEmailNoSecondaryEmail(self):

        self.user.send_email('Subject', 'Message')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), [self.user.email])

    @unittest.skip
    def testSendEmailSecondaryEmail(self):
        self.user.bookerprofile.secondary_email = 'second_email@email.com'
        self.user.save()

        self.user.send_email('Subject', 'Message')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), [self.user.bookerprofile.secondary_email])

    @unittest.skip
    def testSendEmailSecondaryEmailSendToPrimary(self):
        self.user.bookerprofile.secondary_email = 'second_email@email.com'
        self.user.save()

        self.user.send_email('Subject', 'Message', send_to_primary=True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients(), [self.user.email])
