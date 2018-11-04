from unittest import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.views.privilege_categories import PrivilegeCategoryView


class TestPrivilegeCategoryAPI(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        self.category = PrivilegeCategory(name="Base Category")
        self.category.num_days_to_booking = 2
        self.category.can_make_recurring_booking = False
        self.category.max_num_bookings = 5
        self.category.max_num_recurring_bookings = 0
        self.category.save()

    def tearDown(self):
        self.category.delete()

    def testCreatePrivilegeCategorySuccess(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "num_days_to_booking": 4,
                                        "can_make_recurring_booking": "True",
                                        "max_num_bookings": 2,
                                        "max_num_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivilegeCategory.objects.count(), 2)

        created_category = PrivilegeCategory.objects.all()[1]
        self.assertEqual(created_category.name, "Second Tier")
        self.assertEqual(created_category.parent_category, self.category)
        self.assertEqual(created_category.num_days_to_booking, 4)
        self.assertEqual(created_category.can_make_recurring_booking, True)
        self.assertEqual(created_category.max_num_bookings, 2)
        self.assertEqual(created_category.max_num_recurring_bookings, 3)

    def testCreatePrivilegeCategoryInvalidPayload(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": 4,
                                        "parent_category": "WrongFormat",
                                        "num_days_to_booking": 4,
                                        "can_make_recurring_booking": "True",
                                        "max_num_bookings": 2,
                                        "max_num_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PrivilegeCategory.objects.count(), 1)

    def testCreatePrivilegeCategoryNotAuthorized(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "num_days_to_booking": 4,
                                        "can_make_recurring_booking": "True",
                                        "max_num_bookings": 2,
                                        "max_num_recurring_bookings": 3
                                    },
                                    format="json")

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PrivilegeCategory.objects.count(), 1)
