from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestLogout(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.request_factory = APIRequestFactory()
        self.username = 'John'
        self.email = 'JohnDoe@gmail.com'
        self.password = 'johnsVerySafePassword'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def tearDown(self):
        pass

    def testLogout(self):
        authorization = 'Token {}'.format(self.token)
        self.client.get('/logout', HTTP_AUTHORIZATION=authorization)
        try:
            token = Token.objects.get(user=self.user)
            self.fail('Token was not removed')
        except Token.DoesNotExist:
            self.assertTrue('Token has been removed on logout')
