import responses
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from apps.accounts.models.VerificationToken import VerificationToken


class TestResetPassword(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username = 'test_1'
        self.email = 'test@email.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, make_password(self.password))
        self.user.save()

    def tearDown(self):
        pass

    @responses.activate
    def testResetPasswordSuccess(self):
        data = dict(
            username=self.username
        )

        response = self.client.post('/reset_password', data)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username=self.username)
        self.assertTrue(VerificationToken.objects.filter(user=user).exists())

    def testResetPasswordFailure(self):
        data = dict(
            username="NoneExist"
        )

        response = self.client.post('/reset_password', data)
        self.assertEqual(response.status_code, 400)
        user = User.objects.get(username=self.username)
        self.assertFalse(VerificationToken.objects.filter(user=user).exists())

    def testResetPasswordWithSameUsername(self):
        data = dict(
            username=self.username
        )

        response = self.client.post('/reset_password', data)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username=self.username)
        self.assertTrue(VerificationToken.objects.filter(user=user).exists())

        response_again = self.client.post('/reset_password', data)
        self.assertEqual(response_again.status_code, 201)
        user = User.objects.get(username=self.username)
        self.assertTrue(VerificationToken.objects.filter(user=user).exists())
