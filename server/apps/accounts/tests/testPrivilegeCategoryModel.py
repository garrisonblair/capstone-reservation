from datetime import time

from django.test import TestCase

from ..models.PrivilegeCategory import PrivilegeCategory, PrivilegeMerger


class TestPrivilegeCategoryModel(TestCase):

    def setUp(self):
        self.category_1 = PrivilegeCategory(name="Base Category")
        self.category_1.max_days_until_booking = 2
        self.category_1.can_make_recurring_booking = False
        self.category_1.max_bookings = 5
        self.category_1.max_recurring_bookings = 2
        self.category_1.booking_start_time = time(10, 0, 0)
        self.category_1.booking_end_time = time(23, 0, 0)
        self.category_1.save()

        self.category_2 = PrivilegeCategory(name="Second Category")
        self.category_2.max_days_until_booking = 4
        self.category_2.can_make_recurring_booking = True
        self.category_2.max_bookings = 3
        self.category_2.max_recurring_bookings = 4
        self.category_2.booking_start_time = time(9, 0, 0)
        self.category_2.booking_end_time = time(22, 0, 0)
        self.category_2.save()

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

        privilege_category = PrivilegeCategory(name="Specific Category", parent_category=self.category_1)

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

    def testPrivilegeMerger(self):
        merger = PrivilegeMerger([self.category_1, self.category_2])

        self.assertEqual(merger.get_parameter("max_days_until_booking"), 4)
        self.assertEqual(merger.get_parameter("can_make_recurring_booking"), True)
        self.assertEqual(merger.get_parameter("max_bookings"), 5)
        self.assertEqual(merger.get_parameter("max_recurring_bookings"), 4)
        self.assertEqual(merger.get_parameter("booking_start_time"), time(9, 0, 0))
        self.assertEqual(merger.get_parameter("booking_end_time"), time(23, 0, 0))

    def testSetDefaultPrivilegeCategory(self):
        category1 = PrivilegeCategory(name="C1", is_default=True)
        category1.save()

        category2 = PrivilegeCategory(name="C2", is_default=True)
        category2.save()

        category1.refresh_from_db()

        self.assertFalse(category1.is_default)
        self.assertTrue(category2.is_default)
