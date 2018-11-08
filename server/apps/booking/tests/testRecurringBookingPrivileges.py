from django.test import TestCase
from datetime import date, time, timedelta
import datetime

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from ..models.Booking import RecurringBooking
from apps.groups.models.Group import Group
from apps.accounts.exceptions import PrivilegeError
from apps.util.mock_datetime import mock_datetime


class TestBookingPrivileges(TestCase):

    def setUp(self):
        self.p_c_booker = PrivilegeCategory(name="Booker Category")
        self.p_c_booker.max_days_until_booking = 3
        self.p_c_booker.max_bookings = 2
        self.p_c_booker.booking_start_time = time(9, 0, 0)
        self.p_c_booker.booking_end_time = time(22, 0, 0)
        self.p_c_booker.save()

        self.booker = Booker(booker_id="11111111")
        self.booker.save()
        self.booker.privilege_categories.add(self.p_c_booker)
        self.booker.save()

        self.p_c_group = PrivilegeCategory(name="Group Category")
        self.p_c_group.max_days_until_booking = 5
        self.p_c_group.max_bookings = 1
        self.p_c_group.booking_start_time = time(8, 0, 0)
        self.p_c_group.booking_end_time = time(23, 0, 0)
        self.p_c_group.save()

        self.group = Group(name="Group 1",
                           is_verified=True,
                           privilege_category=self.p_c_group)
        self.group.save()
        self.group.bookers.add(self.booker)
        self.group.save()

        self.room = Room(room_id="H916-01")
        self.room.save()

    def testRecurringBookingAllowedBooker(self):
        self.p_c_booker.can_make_recurring_booking = True
        self.p_c_booker.max_recurring_bookings = 2
        self.p_c_booker.save()
        date_in_2_weeks = date.today() + timedelta(days=14)

        RecurringBooking.objects.create_recurring_booking(
            start_date=date.today(),
            end_date=date_in_2_weeks,
            start_time=time(12, 0, 0),
            end_time=time(14, 0, 0),
            room=self.room,
            group=None,
            booker=self.booker,
            skip_conflicts=False
        )

        self.assertEqual(self.booker.recurringbooking_set.count(), 1)

    def testRecurringBookingNotAllowedBooker(self):
        self.p_c_booker.can_make_recurring_booking = False
        self.p_c_booker.max_recurring_bookings = 0
        self.p_c_booker.save()
        date_in_2_weeks = date.today() + timedelta(days=14)

        with self.assertRaises(PrivilegeError):
            RecurringBooking.objects.create_recurring_booking(
                start_date=date.today(),
                end_date=date_in_2_weeks,
                start_time=time(12, 0, 0),
                end_time=time(14, 0, 0),
                room=self.room,
                group=None,
                booker=self.booker,
                skip_conflicts=False
            )

        self.assertEqual(self.booker.recurringbooking_set.count(), 0)

    def testRecurringBookingAllowedGroup(self):
        self.p_c_group.can_make_recurring_booking = True
        self.p_c_group.max_recurring_bookings = 2
        self.p_c_group.save()
        date_in_2_weeks = date.today() + timedelta(days=14)

        RecurringBooking.objects.create_recurring_booking(
            start_date=date.today(),
            end_date=date_in_2_weeks,
            start_time=time(12, 0, 0),
            end_time=time(14, 0, 0),
            room=self.room,
            group=self.group,
            booker=self.booker,
            skip_conflicts=False
        )

        self.assertEqual(self.booker.recurringbooking_set.count(), 1)

    def testRecurringBookingNotAllowedGroup(self):
        self.p_c_group.can_make_recurring_booking = False
        self.p_c_group.max_recurring_bookings = 0
        self.p_c_group.save()
        date_in_2_weeks = date.today() + timedelta(days=14)

        with self.assertRaises(PrivilegeError):
            RecurringBooking.objects.create_recurring_booking(
                start_date=date.today(),
                end_date=date_in_2_weeks,
                start_time=time(12, 0, 0),
                end_time=time(14, 0, 0),
                room=self.room,
                group=self.group,
                booker=self.booker,
                skip_conflicts=False
            )

        self.assertEqual(self.booker.recurringbooking_set.count(), 0)

    def testTooManyRecurringBookingsBooker(self):
        self.p_c_booker.can_make_recurring_booking = True
        self.p_c_booker.max_recurring_bookings = 1
        self.p_c_booker.save()
        date_in_2_weeks = date.today() + timedelta(days=14)

        with mock_datetime(datetime.datetime(date.today().year,
                                             date.today().month,
                                             date.today().day,
                                             11, 30, 0, 0), datetime):
            RecurringBooking.objects.create_recurring_booking(
                start_date=date.today(),
                end_date=date_in_2_weeks,
                start_time=time(12, 0, 0),
                end_time=time(14, 0, 0),
                room=self.room,
                group=None,
                booker=self.booker,
                skip_conflicts=False
            )

            try:
                RecurringBooking.objects.create_recurring_booking(
                    start_date=date.today(),
                    end_date=date_in_2_weeks,
                    start_time=time(16, 0, 0),
                    end_time=time(18, 0, 0),
                    room=self.room,
                    group=None,
                    booker=self.booker,
                    skip_conflicts=False
                )
            except PrivilegeError as error:
                self.assertEqual(error.message, self.p_c_booker.get_error_text("max_recurring_bookings"))

        self.assertEqual(self.booker.recurringbooking_set.count(), 1)

    def testTooManyRecurringBookingsGroup(self):
        self.p_c_group.can_make_recurring_booking = True
        self.p_c_group.max_recurring_bookings = 2
        self.p_c_group.save()
        date_in_2_weeks = date.today() + timedelta(days=14)

        RecurringBooking.objects.create_recurring_booking(
            start_date=date.today(),
            end_date=date_in_2_weeks,
            start_time=time(12, 0, 0),
            end_time=time(14, 0, 0),
            room=self.room,
            group=self.group,
            booker=self.booker,
            skip_conflicts=False
        )

        RecurringBooking.objects.create_recurring_booking(
            start_date=date.today(),
            end_date=date_in_2_weeks,
            start_time=time(16, 0, 0),
            end_time=time(18, 0, 0),
            room=self.room,
            group=self.group,
            booker=self.booker,
            skip_conflicts=False
        )

        with mock_datetime(datetime.datetime(date.today().year,
                                             date.today().month,
                                             date.today().day,
                                             11, 30, 0, 0), datetime):
            try:
                RecurringBooking.objects.create_recurring_booking(
                    start_date=date.today(),
                    end_date=date_in_2_weeks,
                    start_time=time(20, 0, 0),
                    end_time=time(22, 0, 0),
                    room=self.room,
                    group=self.group,
                    booker=self.booker,
                    skip_conflicts=False
                )
            except PrivilegeError as error:
                self.assertEqual(error.message, self.p_c_group.get_error_text("max_recurring_bookings"))

        self.assertEqual(self.group.recurringbooking_set.count(), 2)
