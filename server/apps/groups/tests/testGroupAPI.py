import unittest
import datetime
from collections import OrderedDict

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status


from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.groups.models.Group import Group
from apps.groups.models.GroupInvitation import GroupInvitation
from apps.groups.views.groups import GroupList, GroupCreate, RemoveMembers, InviteMembers, LeaveGroup


class GroupAPITest(TestCase):
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

        self.user_2 = User.objects.create_user(username="fred",
                                               email="fred@email.com",
                                               password='safe password')
        self.user_2.save()

        self.group1 = Group(name="Group1", owner=self.user)
        self.group1.save()
        self.group1.members.add(self.user)
        self.group1.save()

        self.group2 = Group(name="The Beatles", owner=self.user)
        self.group2.save()
        self.group2.members.add(self.user)
        self.group2.save()

        self.category = PrivilegeCategory(is_default=True)
        self.category.max_days_until_booking = 2
        self.category.can_make_recurring_booking = False
        self.category.max_num_days_with_bookings = 5
        self.category.max_num_bookings_for_date = 2
        self.category.max_recurring_bookings = 0
        self.category.booking_start_time = datetime.time(8, 0)
        self.category.booking_end_time = datetime.time(23, 0)
        self.category.save()

    def testGetGroups(self):
        request = self.factory.get("/groups")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = GroupList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.group1.name)
        self.assertEqual(response.data[1]["name"], self.group2.name)

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

        group = Group.objects.get(name="The Group Name", owner=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user in group.members.all())
        self.assertEqual(group.owner, self.user)

    @unittest.skip
    def testInviteMembers(self):
        request = self.factory.post("group/1/invite_members",
                                    {
                                        "invited_bookers": [self.user_2.id]
                                    })
        force_authenticate(request, user=self.user)

        response = InviteMembers.as_view()(request, self.group1.id)

        try:
            invitation = GroupInvitation.objects.get(invited_booker=self.user_2, group=self.group1)
        except GroupInvitation.DoesNotExist:
            self.fail()

        self.assertTrue(True)

    def testLeaveGroupNotOwner(self):

        self.group1 = Group(name="Group1", owner=self.user)
        self.group1.save()
        self.group1.members.add(self.user)
        self.group1.save()

        self.assertEqual(len(self.group1.members.all()), 1)

        self.group1.members.add(self.user_2)
        self.group1.save()

        self.assertEqual(len(self.group1.members.all()), 2)

        request = self.factory.post("group/" + str(self.group1.id) + "/leave_group",
                                    {
                                    }, format="json")

        force_authenticate(request, user=self.user_2)

        response = LeaveGroup.as_view()(request, self.group1.id)

        # self.group1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 1)
        self.assertTrue(self.user in self.group1.members.all())

    def testLeaveGroupOwner(self):

        self.group1 = Group(name="Group1", owner=self.user)
        self.group1.save()
        self.group1.members.add(self.user)
        self.group1.save()

        self.assertEqual(len(self.group1.members.all()), 1)

        self.group1.members.add(self.user_2)
        self.group1.save()

        self.assertEqual(len(self.group1.members.all()), 2)

        request = self.factory.post("group/" + str(self.group1.id) + "/leave_group",
                                    {
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = LeaveGroup.as_view()(request, self.group1.id)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 0)
        self.assertFalse(self.user in self.group1.members.all())

    def testRemoveMember(self):
        self.group1.members.add(self.user2)
        self.group1.save()

        request = self.factory.post("group/" + str(self.group1.id) + "/remove_members",
                                    {
                                        "members": [self.user2.id]
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = RemoveMembers.as_view()(request, self.group1.id)

        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 1)

        self.assertTrue(self.user_2 not in self.group1.members.all())

    def testAttemptRemoveOwner(self):
        self.group1 = Group(name="Group1", owner=self.user)
        self.group1.save()
        self.group1.members.add(self.user)
        self.group1.save()

        request = self.factory.post("group/" + str(self.group1.id) + "/remove_members",
                                    {
                                        "members": [self.user.id]
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = RemoveMembers.as_view()(request, self.group1.id)

        self.group1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(self.group1.members.all()), 1)

        self.assertTrue(self.user in self.group1.members.all())
