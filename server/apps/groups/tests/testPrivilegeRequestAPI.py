import datetime

from django.test.testcases import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory
from django.core import mail

from apps.groups.models.PrivilegeRequest import PrivilegeRequest
from apps.groups.models.Group import Group
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.User import User
from apps.util.mock_datetime import mock_datetime
from apps.groups.views.group_privileges import ApprovePrivilegeRequest, PrivilegeRequestCreate, DenyPrivilegeRequest


class PrivilegeRequestTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.owner = User.objects.create_user(username="john",
                                              email="john@email.com")
        self.owner.save()

        self.category = PrivilegeCategory(name="Category")
        self.category.save(bypass_validation=True)

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

    def testPrivilegeRequestCreateUnauthorized(self):
        request = self.factory.post("/request_privilege",
                                    {
                                        "group": self.group.id,
                                        "privilege_category": self.category.id
                                    },
                                    format="json")

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

        body = "Your request for group privileges has been approved.\n" \
               "\n" \
               "Group: Queen\n" \
               "Privilege Category: Category\n" \
               "\n" \
               "You can view your booking privileges on your account"
        self.assertEqual(mail.outbox[0].body, body)

        db_privilege_request = PrivilegeRequest.objects.get(id=privilege_request.id)

        self.assertEqual(db_privilege_request.status, PrivilegeRequest.AP)

    def testApprovePrivilegeRequestUnauthorized(self):
        privilege_request = PrivilegeRequest(group=self.group, privilege_category=self.category)
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            privilege_request.save()

        request = self.factory.post("/approve_privilege_request",
                                    {
                                        "privilege_request": privilege_request.id
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = ApprovePrivilegeRequest.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)

    def testDenyPrivilegeRequest(self):
        privilege_request = PrivilegeRequest(group=self.group, privilege_category=self.category)
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            privilege_request.save()

        request = self.factory.post("/deny_privilege_request",
                                    {
                                        "privilege_request": privilege_request.id,
                                        "denial_reason": "Test Reason"
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="admin"))

        response = DenyPrivilegeRequest.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Group Booking Privilege Request Denied")

        body = "Your request for group privileges has been denied.\n" \
               "\n" \
               "Group: Queen\n" \
               "Privilege Category: Category\n" \
               "\n" \
               "Reason Provided: Test Reason"
        self.assertEqual(mail.outbox[0].body, body)

        db_privilege_request = PrivilegeRequest.objects.get(id=privilege_request.id)

        self.assertEqual(db_privilege_request.status, PrivilegeRequest.DE)

    def testDenyPrivilegeRequestUnauthorized(self):
        privilege_request = PrivilegeRequest(group=self.group, privilege_category=self.category)
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            privilege_request.save()

        request = self.factory.post("/deny_privilege_request",
                                    {
                                        "privilege_request": privilege_request.id,
                                        "denial_reason": "Test Reason"
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = DenyPrivilegeRequest.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)
