import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.accounts.models.User import User
from apps.accounts.views.user import UserList


class TestUserAPI(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_user(username='admin',
                                              email='admin@email.com',
                                              password='admin',
                                              is_superuser=True)
        self.admin.save()

        self.admin2 = User.objects.create_user(username='admin2',
                                               first_name='admin',
                                               last_name='2',
                                               email='admin2@email.com',
                                               password='admin',
                                               is_superuser=True)
        self.admin2.save()

        self.staff = User.objects.create_user(username='staff1',
                                              first_name='staff',
                                              last_name='1',
                                              email='staff1@email.com',
                                              password='staff',
                                              is_staff=True)
        self.staff.save()

        self.staff2 = User.objects.create_user(username='staff2',
                                               first_name='staff',
                                               last_name='2',
                                               email='staff2@email.com',
                                               password='staff',
                                               is_staff=True)
        self.staff2.save()

        self.user = User.objects.create_user(username='user',
                                             first_name='user',
                                             last_name='1',
                                             email='user1@email.com',
                                             password='user')
        self.user.save()

        self.user2 = User.objects.create_user(username='user2',
                                              first_name='user',
                                              last_name='2',
                                              email='user2@email.com',
                                              password='user')
        self.user2.save()

    def testGetAllUsers(self):
        request = self.factory.get("/users", format="json")
        force_authenticate(request, user=self.admin)
        response = UserList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetAllUsersNotAdmin(self):
        request = self.factory.get("/users", format="json")
        force_authenticate(request, user=self.staff)
        response = UserList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
