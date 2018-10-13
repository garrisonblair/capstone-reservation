from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models.VerificationToken import VerificationToken

class TestVerify(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'admin'
        self.email = 'admin@email.com'
        self.password = 'admin'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = VerificationToken.objects.create(user=self.user)

    def tearDown(self):
        pass

    def testVerify(self):
        data = dict(
            token=self.token.token
        )
        response = self.client.post('/verify', data)
        assert response.status_code == 200

        try:
            verification_token = VerificationToken.objects.get(token=self.token)
        except VerificationToken.DoesNotExist:
            self.fail('Token DNE')

        assert verification_token.user == self.user
        assert self.user.is_active == True
        self.assertTrue('User is verified')


