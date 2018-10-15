from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestUserUpdate(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'admin'
        self.email = 'admin@email.com'
        self.password = 'admin'
        self.user = User.objects.create_user(self.username, self.email, make_password(self.password))
        self.token = Token.objects.create(user=self.user)
        self.new_password = 'oneringtorulethemall'
        self.new_email = 'bilbo@baggins.com'

    def tearDown(self):
        pass

    def testUserUpdate(self):
        authorization = 'Token {}'.format(self.token)
        data = dict(
            password=self.new_password,
            email=self.new_email
        )

        response = self.client.patch('/user/{}'.format(self.user.id), data, HTTP_AUTHORIZATION=authorization)

        assert response.status_code == 200

        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            pass

        check_password(self.new_password, user.password) == True
        assert user.email == self.new_email
        self.assertTrue('User is updated')


