from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
from apps.groups.models.Group import Group

from ..views.groups import GroupList, GroupCreate, AddMembers, RemoveMembers


class RoomAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        self.booker = Booker(booker_id="j_lenn")
        self.booker.user = self.user
        self.booker.save()

        self.booker_2 = Booker(booker_id="booker_2")
        self.booker_2.save()

        self.group1 = Group(name="Group1", owner=self.booker)
        self.group1.save()
        self.group1.members.add(self.booker)
        self.group1.save()

        self.group2 = Group(name="The Beatles", owner=self.booker)
        self.group2.save()
        self.group2.members.add(self.booker)
        self.group2.save()

    def testGetGroups(self):
        request = self.factory.get("/groups")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = GroupList.as_view()(request)
        response_data = [
            {
                'members': ['j_lenn'],
                'owner': 'j_lenn',
                'id': 1,
                'is_verified': False,
                'name': 'Group1',
                'privilege_category': None
            },
            {
                'members': ['j_lenn'],
                'owner': 'j_lenn',
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

    def testCreateGroups(self):
        request = self.factory.post("/group",
                                    {
                                        "name": "The Group Name",
                                        "owner": self.user.booker
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = GroupCreate.as_view()(request)

        group = Group.objects.get(name="The Group Name", owner=self.user.booker)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user.booker in group.members.all())
        self.assertEqual(group.owner, self.user.booker)

    def testAddMember(self):
        request = self.factory.post("/group/1/add_members",
                                    {
                                        "members": ["booker_2"]
                                    }, format="json")
        force_authenticate(request, user=self.user)

        response = AddMembers.as_view()(request, 1)

        group = Group.objects.get(id=1)

        self.assertEqual(len(group.members.all()), 2)
        self.assertTrue(self.booker_2 in group.members.all())

    def testRemoveMember(self):
        self.group1.members.add(self.booker_2)
        self.group1.save()

        request = self.factory.post("group/" + str(self.group1.id) + "/remove_members",
                                    {
                                    "members": ["booker_2"]
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = RemoveMembers.as_view()(request, self.group1.id)

        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 1)
        self.assertTrue(self.booker_2 not in self.group1.members.all())
