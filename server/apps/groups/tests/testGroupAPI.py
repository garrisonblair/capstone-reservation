from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
from apps.groups.models.Group import Group

from ..views.groups import GroupList


class RoomAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        booker = Booker(booker_id="j_lenn")
        booker.user = self.user
        booker.save()

        self.group1 = Group(name="Group1")
        self.group1.save()
        self.group1.bookers.add(booker)
        self.group1.save()

        self.group2 = Group(name="The Beatles")
        self.group2.save()
        self.group2.bookers.add(booker)
        self.group2.save()

    def testGetGroups(self):
        request = self.factory.get("/groups")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = GroupList.as_view()(request)
        response_data = [
            {
                'bookers': ['j_lenn'],
                'id': 1,
                'is_verified': False,
                'name': 'Group1',
                'privilege_category': None
            },
            {
                'bookers': ['j_lenn'],
                'id': 2,
                'is_verified': False,
                'name': 'The Beatles',
                'privilege_category': None
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def testGetGroupsFailureUnauthorized(self):
        request = self.factory.get("/groups")
        response = GroupList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
