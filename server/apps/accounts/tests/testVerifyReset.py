from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from apps.accounts.models.VerificationToken import VerificationToken

from ..models.User import User
from ..views.verify_reset import VerifyResetView


class TestVerifyReset(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.username = 'test'
        self.email = 'test@email.com'
        self.password = 'old_password'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()
        self.token = VerificationToken.objects.create(user=self.user)

    def tearDown(self):
        pass

    def testVerifyResetURL(self):
        new_password = "new_password"
        data = dict(
            token=self.token.token,
            password=new_password
        )
        response = self.client.post('/verify_reset', data)
        assert response.status_code == 200

    def testVerifyResetSuccess(self):
        new_password = "new_password"
        request = self.factory.post('/VerificationToken',
                                    {
                                        "token": self.token.token,
                                        "password": new_password
                                    },
                                    format="json")

        response = VerifyResetView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username=self.username)
        self.assertTrue(check_password(new_password, user.password))

    def testVerifyResetFailure(self):
        new_password = "new_password"
        request = self.factory.post('/VerificationToken',
                                    {
                                        "token": "invalid_token",
                                        "password": new_password
                                    },
                                    format="json")

        response = VerifyResetView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=self.username)
        self.assertTrue(check_password(self.password, user.password))
