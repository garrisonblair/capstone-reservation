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

        self.user = User.objects.create_user(username='jerry',
                                             email='jseinfeld@email.com',
                                             password='constanza')
        self.user.is_superuser = True
        self.user.save()

        self.category = PrivilegeCategory(name="Base Category")
        self.category.max_days_until_booking = 2
        self.category.can_make_recurring_booking = False
        self.category.max_bookings = 5
        self.category.max_recurring_bookings = 0
        self.category.save()

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def testCreatePrivilegeCategorySuccess(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "max_days_until_booking": 4,
                                        "can_make_recurring_booking": True,
                                        "max_bookings": 2,
                                        "max_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivilegeCategory.objects.count(), 2)

        created_category = PrivilegeCategory.objects.all()[1]
        self.assertEqual(created_category.get_parameter("name"), "Second Tier")
        self.assertEqual(created_category.get_parameter("parent_category"), self.category)
        self.assertEqual(created_category.get_parameter("max_days_until_booking"), 4)
        self.assertEqual(created_category.get_parameter("can_make_recurring_booking"), True)
        self.assertEqual(created_category.get_parameter("max_bookings"), 2)
        self.assertEqual(created_category.get_parameter("max_recurring_bookings"), 3)

    def testCreatePrivilegeCategorySuccessPartialParams(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "max_days_until_booking": None,
                                        "can_make_recurring_booking": True,
                                        "max_bookings": 2,
                                        "max_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivilegeCategory.objects.count(), 2)

        created_category = PrivilegeCategory.objects.all()[1]
        self.assertEqual(created_category.get_parameter("name"), "Second Tier")
        self.assertEqual(created_category.get_parameter("parent_category"), self.category)
        # Uses parent category for num_days_to_booking
        self.assertEqual(created_category.get_parameter("max_days_until_booking"), self.category.max_days_until_booking)
        self.assertEqual(created_category.get_parameter("can_make_recurring_booking"), True)
        self.assertEqual(created_category.get_parameter("max_bookings"), 2)
        self.assertEqual(created_category.get_parameter("max_recurring_bookings"), 3)

    def testCreatePrivilegeCategorySuccessPartialParamsMissingBoolean(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "max_days_until_booking": 4,
                                        "can_make_recurring_booking": None,
                                        "max_bookings": 2,
                                        "max_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivilegeCategory.objects.count(), 2)

        created_category = PrivilegeCategory.objects.all()[1]
        self.assertEqual(created_category.get_parameter("name"), "Second Tier")
        self.assertEqual(created_category.get_parameter("parent_category"), self.category)
        self.assertEqual(created_category.get_parameter("max_days_until_booking"), 4)
        # Uses parent category for can_make_recurring_booking
        self.assertEqual(created_category.get_parameter("can_make_recurring_booking"), False)
        self.assertEqual(created_category.get_parameter("max_bookings"), 2)
        self.assertEqual(created_category.get_parameter("max_recurring_bookings"), 3)

    def testCreatePrivilegeCategoryInvalidPayload(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": 4,
                                        "parent_category": "WrongFormat",
                                        "max_days_until_booking": 4,
                                        "can_make_recurring_booking": "True",
                                        "max_bookings": 2,
                                        "max_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PrivilegeCategory.objects.count(), 1)

    def testCreatePrivilegeCategoryNotAuthorized(self):
        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "max_days_until_booking": 4,
                                        "can_make_recurring_booking": "True",
                                        "max_bookings": 2,
                                        "max_recurring_bookings": 3
                                    },
                                    format="json")

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PrivilegeCategory.objects.count(), 1)

    def testViewAllCategories(self):
        self.category1 = PrivilegeCategory(name="Second Tier")
        self.category1.max_days_until_booking = 4
        self.category1.can_make_recurring_booking = True
        self.category1.max_bookings = 8
        self.category1.max_recurring_bookings = 2
        self.category1.save()

        request = self.factory.get("privilege_categories",
                                   {
                                   },
                                   format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.category1.delete()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_categories = response.data
        self.assertEqual(len(returned_categories), 2)

    def testViewCategoriesByName(self):
        self.category1 = PrivilegeCategory(name="Second Tier")
        self.category1.max_days_until_booking = 4
        self.category1.can_make_recurring_booking = True
        self.category1.max_bookings = 8
        self.category1.max_recurring_bookings = 2
        self.category1.save()

        request = self.factory.get("privilege_categories",
                                   {
                                       "name": "Base Category"
                                   },
                                   format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.category1.delete()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_categories = response.data
        self.assertEqual(len(returned_categories), 1)

    def testViewCategoriesByNameNoResults(self):
        self.category1 = PrivilegeCategory(name="Second Tier")
        self.category1.max_days_until_booking = 4
        self.category1.can_make_recurring_booking = True
        self.category1.max_bookings = 8
        self.category1.max_recurring_bookings = 2
        self.category1.save()

        request = self.factory.get("privilege_categories",
                                   {
                                       "name": "Premium Category"
                                   },
                                   format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.category1.delete()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testCreateFailureUnauthorized(self):
        self.user.is_superuser = False
        self.user.save()

        request = self.factory.post("/privilege_categories",
                                    {
                                        "name": "Second Tier",
                                        "parent_category": self.category.id,
                                        "max_days_until_booking": None,
                                        "can_make_recurring_booking": True,
                                        "max_bookings": 2,
                                        "max_recurring_bookings": 3
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testViewFailureUnauthorized(self):
        self.user.is_superuser = False
        self.user.save()

        request = self.factory.get("privilege_categories",
                                   {
                                   },
                                   format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
