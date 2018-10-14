import requests
import responses
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.serializers.UserSerializer import UserSerializerLogin


class TestRegister(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'sauron'
        self.email = 'sauron@lotr.com'
        self.password = 'precious'
        self.user = User.objects.create_user(self.username, self.email, make_password(self.password))

    def tearDown(self):
        pass

    @responses.activate
    def testRegister(self):
        json = UserSerializerLogin(self.user).data
        data = dict(
            username=self.username
        )
        responses.add(responses.POST, 'http://localhost:8000/register', json=json, status=201)
        response = requests.post('http://localhost:8000/register', data=data)

        assert response.status_code == 201

        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            self.fail('User DNE')

        assert user.username == self.username
        self.assertTrue('User is registered')


