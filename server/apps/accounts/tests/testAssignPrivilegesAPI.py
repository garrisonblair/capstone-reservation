import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.accounts.models.BookerProfile import BookerProfile
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.views.assign_privileges import PrivilegeCategoriesAssignManual


class AssignPrivilegesTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='admin',
                                             email='admin@email.com',
                                             password='admin')
        self.user.is_superuser = True
        self.user.save()

        self.user1 = User.objects.create_user(username="user1",
                                              email="user1@email.com",
                                              password="user1")
        self.user1.save()

        self.user2 = User.objects.create_user(username="user2",
                                              email="user2@email.com",
                                              password="user2")
        self.user2.save()

        self.category1 = PrivilegeCategory(name="Base Category")
        self.category1.max_days_until_booking = 2
        self.category1.can_make_recurring_booking = False
        self.category1.max_recurring_bookings = 0
        self.category1.booking_start_time = datetime.time(8, 0)
        self.category1.booking_end_time = datetime.time(23, 0)
        self.category1.save(bypass_validation=True)

    def testAssignPrivilegeSuccess(self):
        body = {
            "users": [self.user1.id, self.user2.id],
            "privilege_category": self.category1.id
        }

        request = self.factory.patch("/assign_privilege", body, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))
        response = PrivilegeCategoriesAssignManual.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.bookerprofile.privilege_categories.count(), 1)
        self.assertEqual(self.user1.bookerprofile.privilege_categories.all()[0], self.category1)
        self.assertEqual(self.user2.bookerprofile.privilege_categories.count(), 1)
        self.assertEqual(self.user2.bookerprofile.privilege_categories.all()[0], self.category1)

    def testAssignPrivilegesWrongUser(self):
        body = {
            "users": [self.user1.id, 10000],
            "privilege_category": self.category1.id
        }

        request = self.factory.patch("/assign_privilege", body, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))
        response = PrivilegeCategoriesAssignManual.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.bookerprofile.privilege_categories.count(), 1)
        self.assertEqual(self.user1.bookerprofile.privilege_categories.all()[0], self.category1)
        self.assertEqual(self.user2.bookerprofile.privilege_categories.count(), 0)
        self.assertEqual(response.data, [10000])

    def testAssignPrivilegesWrongCategory(self):
        body = {
            "users": [self.user1.id, self.user2.id],
            "privilege_category": 12
        }

        request = self.factory.patch("/assign_privilege", body, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))
        response = PrivilegeCategoriesAssignManual.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user1.bookerprofile.privilege_categories.count(), 0)
        self.assertEqual(self.user2.bookerprofile.privilege_categories.count(), 0)