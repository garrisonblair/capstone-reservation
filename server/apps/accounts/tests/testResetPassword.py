import requests
import responses
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from apps.accounts.serializers.user import UserSerializerLogin

from ..views.reset_password import ResetPasswordView


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
    def testResetPasswordURL(self):
        json = UserSerializerLogin(self.user).data
        data = dict(
            username=self.username
        )
        responses.add(responses.POST, 'http://localhost:8000/reset_password', json=json, status=201)
        response = requests.post('http://localhost:8000/reset_password', data=data)

        assert response.status_code == 201

    def testResetPasswordSuccess(self):
        request = self.factory.post('/user',
                                    {
                                        "username": self.username
                                    },
                                    format="json")

        response = ResetPasswordView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testResetPasswordFailure(self):
        request = self.factory.post('/user',
                                    {
                                        "username": "NoneExist"
                                    },
                                    format="json")

        response = ResetPasswordView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testResetPasswordWithSameAC(self):
        request = self.factory.post('/user',
                                    {
                                        "username": self.username
                                    },
                                    format="json")

        response = ResetPasswordView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        request_again = self.factory.post('/user',
                                          {
                                                "username": self.username
                                          },
                                          format="json")
        response_again = ResetPasswordView.as_view()(request_again)
        self.assertEqual(response_again.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
