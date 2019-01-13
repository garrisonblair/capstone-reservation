from django.test import TestCase

from apps.accounts.models.BookerProfile import BookerProfile
from apps.accounts.models.User import User


class TestBooker(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBookerProfileCreation(self):
        user = User.objects.create_user(username="f_daigl",
                                        email="fred@email.com",
                                        password="safePassword")

        read_student = BookerProfile.objects.get(user=user)

        self.assertEqual(read_student.user, user)
