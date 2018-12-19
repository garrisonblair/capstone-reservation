import datetime

from django.test.testcases import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory
from django.core import mail

from apps.groups.models.PrivilegeRequest import PrivilegeRequest
from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.Booker import Booker
from apps.util.mock_datetime import mock_datetime
from apps.groups.views.group_privileges import ApprovePrivilegeRequest, PrivilegeRequestCreate


class PrivilegeRequestTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.owner = Booker.objects.create(booker_id=11111111)
        self.owner.save()
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@test.com',
                                             password='password')
        self.user.save()
        self.owner.user = self.user
        self.owner.save()

        self.category = PrivilegeCategory(name="Category")
        self.category.save()

        self.group = Group(name="Queen", is_verified=False, owner=self.owner)
        self.group.save()
        self.group.members.add(self.owner)
        self.group.save()

        self.admin = User.objects.create_user(username='admin',
                                              email="admin@email.com",
                                              password='admin')
        self.admin.is_superuser = True
        self.admin.save()

    def testPrivilegeRequestCreate(self):
        request = self.factory.post("/request_privilege",
                                    {
                                        "group": self.group.id,
                                        "privilege_category": self.category.id
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = PrivilegeRequestCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivilegeRequest.objects.count(), 1)

    def testPrivilegeRequestCreateFailure(self):
        request = self.factory.post("/request_privilege",
                                    {
                                        "group": 7,
                                        "privilege_category": self.category.id
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = PrivilegeRequestCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PrivilegeRequest.objects.count(), 0)

    def testPrivilegeRequestCreate(self):
        request = self.factory.post("/request_privilege",
                                    {
                                        "group": self.group.id,
                                        "privilege_category": self.category.id
                                    },
                                    format="json")

        # force_authenticate(request, user=User.objects.get(username="john"))

        response = PrivilegeRequestCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PrivilegeRequest.objects.count(), 0)

    def testApprovePrivilegeRequest(self):
        privilege_request = PrivilegeRequest(group=self.group, privilege_category=self.category)
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            privilege_request.save()

        request = self.factory.post("/approve_privilege_request",
                                    {
                                        "privilege_request": privilege_request.id
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="admin"))

        response = ApprovePrivilegeRequest.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Group Booking Privilege Request Approval")

        db_privilege_request = PrivilegeRequest.objects.get(id=privilege_request.id)

        self.assertEqual(db_privilege_request.status, PrivilegeRequest.AP)
