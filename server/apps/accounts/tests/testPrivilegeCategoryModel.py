from django.test import TestCase

from ..models.PrivilegeCategory import PrivilegeCategory


class TestPrivilegeCategoryModel(TestCase):

    def setUp(self):
        self.category = PrivilegeCategory(name="Base Category")
        self.category.max_days_until_booking = 2
        self.category.can_make_recurring_booking = False
        self.category.max_bookings = 5
        self.category.max_recurring_bookings = 2
        self.category.save()

    def testCreation(self):

        privilege_category = PrivilegeCategory(name="Category 1")
        privilege_category.save()

        read_category = PrivilegeCategory.objects.get(name="Category 1")  # type: PrivilegeCategory

        self.assertEqual(read_category.name, privilege_category.name)
        self.assertEqual(read_category.max_days_until_booking, None)
        self.assertEqual(read_category.can_make_recurring_booking, None)
        self.assertEqual(read_category.max_bookings, None)
        self.assertEqual(read_category.max_recurring_bookings, None)
        self.assertEqual(read_category.booking_start_time, None)
        self.assertEqual(read_category.booking_end_time, None)

    def testParameterDelegation(self):

        privilege_category = PrivilegeCategory(name="Specific Category", parent_category=self.category)

        # set some parameters
        privilege_category.max_days_until_booking = 4
        privilege_category.can_make_recurring_booking = True
        privilege_category.save()

        # Check directly set parameters
        self.assertEqual(privilege_category.get_parameter("max_days_until_booking"), 4)
        self.assertEqual(privilege_category.get_parameter("can_make_recurring_booking"), True)

        # Check delegated parameters
        self.assertEqual(privilege_category.get_parameter("max_bookings"), 5)
        self.assertEqual(privilege_category.get_parameter("max_recurring_bookings"), 2)
