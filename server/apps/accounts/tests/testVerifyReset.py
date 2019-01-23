from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from apps.accounts.models.VerificationToken import VerificationToken

from ..models.User import User


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

    def testVerifyResetSuccess(self):
        new_password = "new_password"
        data = dict(
            token=self.token.token,
            password=new_password
        )
        response = self.client.post('/verify_reset', data)
        assert response.status_code == 200
        user = User.objects.get(username=self.username)
        self.assertTrue(check_password(new_password, user.password))
        self.assertFalse(VerificationToken.objects.filter(user=user).exists())

    def testVerifyResetFailure(self):
        new_password = "new_password"
        data = dict(
            token="invalid_token",
            password=new_password
        )
        response = self.client.post('/verify_reset', data)
        assert response.status_code == 400
        user = User.objects.get(username=self.username)
        self.assertTrue(check_password(self.password, user.password))
