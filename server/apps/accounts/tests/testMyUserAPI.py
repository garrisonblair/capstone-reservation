import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.views.me import MyPrivileges


class TestMyUserAPI(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.category1 = PrivilegeCategory(name="Base Category")
        self.category1.max_days_until_booking = 2
        self.category1.can_make_recurring_booking = False
        self.category1.max_num_days_with_bookings = 5
        self.category1.max_num_bookings_for_date = 2
        self.category1.max_recurring_bookings = 0
        self.category1.booking_start_time = datetime.time(8, 0)
        self.category1.booking_end_time = datetime.time(23, 0)
        self.category1.save()

        self.category2 = PrivilegeCategory(name="Category 2")
        self.category2.max_days_until_booking = 4
        self.category2.can_make_recurring_booking = True
        self.category2.max_num_days_with_bookings = 3
        self.category2.max_num_bookings_for_date = 6
        self.category2.max_recurring_bookings = 1
        self.category2.booking_start_time = datetime.time(8, 0)
        self.category2.booking_end_time = datetime.time(23, 0)
        self.category2.save()

        self.user = User.objects.create_user(username='jerry',
                                             email='jseinfeld@email.com',
                                             password='constanza')
        self.user.save()
        self.user.bookerprofile.privilege_categories.add(self.category1, self.category2)
        self.user.save()

    def testGetMyPrivilegesSuccess(self):
        request = self.factory.get("/my_privileges", format="json")
        force_authenticate(request, user=User.objects.get(username="jerry"))
        response = MyPrivileges.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["max_days_until_booking"], 4)

        self.assertEqual(response.data["me"]["max_num_days_with_bookings"], 5)
        self.assertEqual(response.data["me"]["max_recurring_bookings"], 1)
        self.assertEqual(response.data["me"]["max_num_bookings_for_date"], 6)
        self.assertEqual(response.data["me"]["can_make_recurring_booking"], True)
        self.assertEqual(response.data["me"]["booking_start_time"], datetime.time(8, 0))
        self.assertEqual(response.data["me"]["booking_end_time"], datetime.time(23, 0))
