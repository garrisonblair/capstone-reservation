import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from apps.accounts.models.Booker import Booker
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.views.privilege_categories import MyPrivilegeCategoryList
from apps.accounts.views.privilege_categories import PrivilegeCategoryList
from apps.accounts.views.privilege_categories import PrivilegeCategoryCreate
from apps.accounts.views.privilege_categories import PrivilegeCategoryRetrieveUpdateDestroy


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
        self.category.booking_start_time = datetime.time(8, 0)
        self.category.booking_end_time = datetime.time(23, 0)
        self.category.save()

    def testCreatePrivilegeCategorySuccess(self):
        body = {
            "name": "Second Tier",
            "parent_category": self.category.id,
            "is_default": True,
            "max_days_until_booking": 4,
            "can_make_recurring_booking": True,
            "max_bookings": 2,
            "max_recurring_bookings": 3,
            "booking_start_time": self.category.booking_start_time,
            "booking_end_time": self.category.booking_end_time
        }
        request = self.factory.post("/privilege_category", body, format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = PrivilegeCategoryCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrivilegeCategory.objects.count(), 2)

        created_category = PrivilegeCategory.objects.all()[1]
        self.assertEqual(created_category.get_parameter("name"), "Second Tier")
        self.assertEqual(created_category.get_parameter("parent_category"), self.category)
        self.assertEqual(created_category.get_parameter("is_default"), True)

        self.assertEqual(created_category.get_parameter("max_days_until_booking"), 4)
        self.assertEqual(created_category.get_parameter("can_make_recurring_booking"), True)
        self.assertEqual(created_category.get_parameter("max_bookings"), 2)
        self.assertEqual(created_category.get_parameter("max_recurring_bookings"), 3)
        self.assertEqual(created_category.get_parameter("booking_start_time"), self.category.booking_start_time)
        self.assertEqual(created_category.get_parameter("booking_end_time"), self.category.booking_end_time)

    def testCreatePrivilegeCategorySuccessPartialParams(self):
        body = {
            "name": "Second Tier",
            "parent_category": self.category.id,
            "is_default": False,
            "max_days_until_booking": None,
            "can_make_recurring_booking": True,
            "max_bookings": 2,
            "max_recurring_bookings": 3,
            "booking_start_time": self.category.booking_start_time,
            "booking_end_time": self.category.booking_end_time
        }

        request = self.factory.post("/privilege_category", body, format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = PrivilegeCategoryCreate.as_view()(request)

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
        self.assertEqual(created_category.get_parameter("booking_start_time"), self.category.booking_start_time)
        self.assertEqual(created_category.get_parameter("booking_end_time"), self.category.booking_end_time)

    def testCreatePrivilegeCategorySuccessPartialParamsMissingBoolean(self):
        body = {
            "name": "Second Tier",
            "parent_category": self.category.id,
            "max_days_until_booking": 4,
            "can_make_recurring_booking": None,
            "max_bookings": 2,
            "max_recurring_bookings": 3,
            "booking_start_time": self.category.booking_start_time,
            "booking_end_time": self.category.booking_end_time
        }
        request = self.factory.post("/privilege_categories", body, format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = PrivilegeCategoryCreate.as_view()(request)

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
        self.assertEqual(created_category.get_parameter("booking_start_time"), self.category.booking_start_time)
        self.assertEqual(created_category.get_parameter("booking_end_time"), self.category.booking_end_time)

    def testCreatePrivilegeCategoryInvalidPayload(self):
        body = {
            "name": 4,
            "parent_category": "WrongFormat",
            "max_days_until_booking": 4,
            "can_make_recurring_booking": "True",
            "max_bookings": 2,
            "max_recurring_bookings": 3,
            "booking_start_time": self.category.booking_start_time,
            "booking_end_time": self.category.booking_end_time
        }
        request = self.factory.post("/privilege_categories", body, format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = PrivilegeCategoryCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PrivilegeCategory.objects.count(), 1)

    def testCreatePrivilegeCategoryUnauthorized(self):
        self.user.is_superuser = False
        self.user.save()
        self.user.refresh_from_db()
        client = APIClient()
        client.login(username='jerry', password='constanza')
        token = Token.objects.get_or_create(user=self.user)
        authorization = 'Token {}'.format(token)
        data = {
            "name": "Second Tier",
            "parent_category": self.category.id,
            "max_days_until_booking": 4,
            "can_make_recurring_booking": "True",
            "max_bookings": 2,
            "max_recurring_bookings": 3,
            "booking_start_time": self.category.booking_start_time,
            "booking_end_time": self.category.booking_end_time
        }
        response = client.post(
            "/privilege_categories",
            data,
            HTTP_AUTHORIZATION=authorization,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PrivilegeCategory.objects.count(), 1)

    def testViewAllCategories(self):
        self.category1 = PrivilegeCategory(name="Second Tier")
        self.category1.max_days_until_booking = 4
        self.category1.can_make_recurring_booking = True
        self.category1.max_bookings = 8
        self.category1.max_recurring_bookings = 2
        self.category1.booking_start_time = datetime.time(5, 0)
        self.category1.booking_end_time = datetime.time(12, 0)
        self.category1.save()

        request = self.factory.get("privilege_categories", format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = PrivilegeCategoryList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_categories = response.data
        self.assertEqual(len(returned_categories), 2)

    def testViewCategoriesByName(self):
        self.category1 = PrivilegeCategory(name="Second Tier")
        self.category1.max_days_until_booking = 4
        self.category1.can_make_recurring_booking = True
        self.category1.max_bookings = 8
        self.category1.max_recurring_bookings = 2
        self.category1.booking_start_time = datetime.time(5, 0)
        self.category1.booking_end_time = datetime.time(12, 0)
        self.category1.save()

        params = {
            "name": "Base Category"
        }

        request = self.factory.get("privilege_categories", params, format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = PrivilegeCategoryList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testViewCategoriesByNameNoResults(self):
        self.category1 = PrivilegeCategory(name="Second Tier")
        self.category1.max_days_until_booking = 4
        self.category1.can_make_recurring_booking = True
        self.category1.max_bookings = 8
        self.category1.max_recurring_bookings = 2
        self.category1.booking_start_time = datetime.time(5, 0)
        self.category1.booking_end_time = datetime.time(12, 0)
        self.category1.save()

        request = self.factory.get("privilege_categories",
                                   {
                                       "name": "Premium Category"
                                   },
                                   format="json")

        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryList.as_view()(request)
        self.assertEqual(len(response.data), 0)

    def testViewFailureUnauthorized(self):
        self.user.is_superuser = False
        self.user.save()
        self.user.refresh_from_db()

        request = self.factory.get("privilege_categories")
        force_authenticate(request, user=self.user)
        response = PrivilegeCategoryList.as_view()(request)

        # A permission class returns either 401/403 if the user is not authorized
        self.assertTrue(response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    def testViewBookerPrivileges(self):
        booker = Booker.objects.create(booker_id=11111111, user=self.user)
        self.user.is_superuser = False
        self.user.save()
        self.user.refresh_from_db()

        request = self.factory.get("my_privileges")
        force_authenticate(request, user=self.user)
        response = MyPrivilegeCategoryList.as_view()(request)

        self.assertEqual(len(response.data), 0)

        booker.privilege_categories.add(self.category)
        booker.save()

        request = self.factory.get("my_privileges")
        force_authenticate(request, user=self.user)
        response = MyPrivilegeCategoryList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testUpdateSuccess(self):
        self.user.is_superuser = True
        self.user.save()
        self.user.refresh_from_db()

        self.category.max_bookings = 10
        self.category.max_days_until_booking = 4
        self.category.save()

        data = {
            "name": self.category.name,
            "max_bookings": self.category.max_bookings,
            "max_days_until_booking": self.category.max_days_until_booking
        }

        request = self.factory.patch("privilege_category", data, format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))

        response = PrivilegeCategoryRetrieveUpdateDestroy.as_view()(request, pk=self.category.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_category = PrivilegeCategory.objects.get(name="Base Category")
        # Updated fields
        self.assertEqual(updated_category.max_bookings, self.category.max_bookings)
        self.assertEqual(updated_category.max_days_until_booking, self.category.max_days_until_booking)
        # Unchanged fields
        self.assertEqual(updated_category.booking_start_time, self.category.booking_start_time)
        self.assertEqual(updated_category.booking_end_time, self.category.booking_end_time)
        self.assertEqual(updated_category.can_make_recurring_booking, self.category.can_make_recurring_booking)
        self.assertEqual(updated_category.max_recurring_bookings, self.category.max_recurring_bookings)
