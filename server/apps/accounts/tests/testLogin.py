from rest_framework.test import APIRequestFactory
from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework.authtoken import views
from apps.accounts.views.me import MyUser


class TestLogin(TestCase):

    def setUp(self):
        user = User.objects.create_user('John', 'JohnDoe@gmail.com', 'johnsVerySafePassword')
        user.save()
        pass

    def tearDown(self):
        pass

    def testLogin(self):
        request_factory = APIRequestFactory()
        view = views.obtain_auth_token

        request = request_factory.post('/login', {'username': 'John', 'password': 'johnsVerySafePassword'})

        response = view(request)

        try:
            token = response.data['token']
        except KeyError:
            self.fail('No token retrieved')

        self.assertTrue(token is not None or token is not '')
