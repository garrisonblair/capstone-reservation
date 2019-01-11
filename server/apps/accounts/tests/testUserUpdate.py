from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import unittest

from ..models.PrivilegeCategory import PrivilegeCategory
from ..models.BookerProfile import Booker


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

        self.privilege_category = PrivilegeCategory(name="C1", is_default=True)
        self.privilege_category.save()

    def tearDown(self):
        pass

    @unittest.skip("LDAP issue causes test to run infinite loop if not connected to LDAP")
    def testUserUpdate(self):
        authorization = 'Token {}'.format(self.token)
        data = dict(
            password=self.new_password,
            email=self.new_email,
            booker_id="11111111"
        )

        response = self.client.patch('/user/{}'.format(self.user.id), data, HTTP_AUTHORIZATION=authorization)

        self.assertEqual(response.status_code, 200)

        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist:
            pass

        check_password(self.new_password, user.password) is True
        self.assertEqual(user.email, self.new_email)

        booker = Booker.objects.get(user=user)

        self.assertEqual(self.privilege_category, booker.privilege_categories.all()[0])

        self.assertTrue('User is updated')
