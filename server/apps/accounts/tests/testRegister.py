import responses
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models.VerificationToken import VerificationToken


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
        data = dict(
            username=self.username
        )

        response = self.client.post('/register', data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(VerificationToken.objects.filter(user=self.user).exists())
