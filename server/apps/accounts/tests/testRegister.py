from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class TestRegister(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'ed_tran'  # Must be an actual ENCS username

    def tearDown(self):
        pass

    def testRegister(self):
        data = dict(
            username=self.username
        )
        response = self.client.post('/register', data)

        assert response.status_code == 201

        try:
            user = User.objects.get(username=self.username)
        except Token.DoesNotExist:
            self.fail('User DNE')

        assert user.username == self.username
        self.assertTrue('User is registered')


