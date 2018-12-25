from collections import OrderedDict

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

        self.user2 = User.objects.create_user(username='paul',
                                              email='pmcartney@beatles.com',
                                              password='yellow submarine')

        self.user.save()

        self.user2.save()

        self.booker = Booker(booker_id="j_lenn")
        self.booker.user = self.user
        self.booker.save()

        self.booker_2 = Booker(booker_id="booker_2")
        self.booker_2.user = self.user2
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
            OrderedDict(
                [
                    ('id', 1),
                    ('owner', OrderedDict(
                        [
                            ('booker_id', 'j_lenn'),
                            ('user', OrderedDict(
                                [
                                    ('id', 1),
                                    ('username', 'john'),
                                    ('first_name', ''),
                                    ('last_name', ''),
                                    ('email', 'jlennon@beatles.com'),
                                    ('is_superuser', False),
                                    ('is_staff', False),
                                    ('is_active', True)
                                ])
                             )
                        ])
                     ),
                    ('members', [OrderedDict(
                        [
                            ('booker_id', 'j_lenn'),
                            ('user', OrderedDict(
                                [
                                    ('id', 1),
                                    ('username', 'john'),
                                    ('first_name', ''),
                                    ('last_name', ''),
                                    ('email', 'jlennon@beatles.com'),
                                    ('is_superuser', False),
                                    ('is_staff', False),
                                    ('is_active', True)
                                ])
                             )
                        ])
                    ]),
                    ('name', 'Group1'),
                    ('is_verified', False),
                    ('privilege_category', None)]),
            OrderedDict(
                [
                    ('id', 2),
                    ('owner', OrderedDict(
                        [
                            ('booker_id', 'j_lenn'),
                            ('user', OrderedDict(
                                [
                                    ('id', 1),
                                    ('username', 'john'),
                                    ('first_name', ''),
                                    ('last_name', ''),
                                    ('email', 'jlennon@beatles.com'),
                                    ('is_superuser', False),
                                    ('is_staff', False),
                                    ('is_active', True)
                                ])
                             )
                        ])
                     ),
                    ('members', [OrderedDict(
                        [
                            ('booker_id', 'j_lenn'),
                            ('user', OrderedDict(
                                [
                                    ('id', 1),
                                    ('username', 'john'),
                                    ('first_name', ''),
                                    ('last_name', ''),
                                    ('email', 'jlennon@beatles.com'),
                                    ('is_superuser', False),
                                    ('is_staff', False),
                                    ('is_active', True)
                                ])
                             )
                        ])
                    ]),
                    ('name', 'The Beatles'),
                    ('is_verified', False),
                    ('privilege_category', None)]
            )
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
                                        "name": "The Group Name"
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
                                        "members": [self.booker_2.user.id]
                                    }, format="json")
        force_authenticate(request, user=self.user)

        AddMembers.as_view()(request, 1)

        group = Group.objects.get(id=1)

        self.assertEqual(len(group.members.all()), 2)
        self.assertTrue(self.booker_2 in group.members.all())

    def testRemoveMember(self):
        self.group1.members.add(self.booker_2)
        self.group1.save()

        request = self.factory.post("group/" + str(self.group1.id) + "/remove_members",
                                    {
                                        "members": [self.booker_2.user.id]
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = RemoveMembers.as_view()(request, self.group1.id)

        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 1)
        self.assertTrue(self.booker_2 not in self.group1.members.all())

    def testAttemptRemoveOwner(self):

        self.group1 = Group(name="Group1", owner=self.booker)
        self.group1.save()
        self.group1.members.add(self.booker)
        self.group1.save()

        request = self.factory.post("group/" + str(self.group1.id) + "/remove_members",
                                    {
                                        "members": [self.booker.user.id]
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = RemoveMembers.as_view()(request, self.group1.id)

        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 1)
        self.assertTrue(self.booker in self.group1.members.all())
