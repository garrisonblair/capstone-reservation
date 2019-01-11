from django.test import TestCase
from datetime import date, time, timedelta
import datetime

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.BookerProfile import Booker
from apps.rooms.models.Room import Room
from ..models.Booking import Booking
from apps.groups.models.Group import Group
from apps.accounts.exceptions import PrivilegeError
from apps.util.mock_datetime import mock_datetime


class TestBookingPrivileges(TestCase):

    def setUp(self):
        self.p_c_booker = PrivilegeCategory(name="Booker Category")

        self.p_c_booker.max_days_until_booking = 3
        self.p_c_booker.max_num_days_with_bookings = 2
        self.p_c_booker.max_num_bookings_for_date = 2
        self.p_c_booker.booking_start_time = time(9, 0, 0)
        self.p_c_booker.booking_end_time = time(22, 0, 0)

        self.p_c_booker.save(bypass_validation=True)

        self.booker = Booker(booker_id="11111111")
        self.booker.save()
        self.booker.privilege_categories.add(self.p_c_booker)
        self.booker.save()

        self.p_c_group = PrivilegeCategory(name="Group Category")
        self.p_c_group.max_days_until_booking = 5
        self.p_c_group.max_num_days_with_bookings = 2
        self.p_c_group.max_num_bookings_for_date = 2
        self.p_c_group.booking_start_time = time(8, 0, 0)
        self.p_c_group.booking_end_time = time(23, 0, 0)
        self.p_c_group.save(bypass_validation=True)

        self.group = Group(name="Group 1",
                           is_verified=True,
                           owner=self.booker,
                           privilege_category=self.p_c_group
                           )
        self.group.save()
        self.group.members.add(self.booker)
        self.group.save()

        self.room = Room(name="H916-01")
        self.room.save()

    def testBookingAllowedBooker(self):

        date_in_3_days = date.today() + timedelta(days=3)

        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=date_in_3_days,
                          start_time=time(9, 30, 0),
                          end_time=time(21, 30, 0)
                          )

        try:
            booking.save()
        except PrivilegeError:
            self.fail("Booking should be saved, no privilege contradiction.")
            return

        self.assertTrue(True)

    def testBookingAllowedGroup(self):

        date_in_5_days = date.today() + timedelta(days=5)

        booking = Booking(booker=self.booker,
                          group=self.group,
                          room=self.room,
                          date=date_in_5_days,
                          start_time=time(8, 30, 0),
                          end_time=time(22, 30, 0),
                          )

        try:
            booking.save()
        except PrivilegeError:
            self.fail("Booking should be saved, no privilege contradiction.")
            return

        self.assertTrue(True)

    def testBookingTooEarlyBooker(self):
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=date.today(),
                          start_time=time(8, 30, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_booker.get_error_text("booking_start_time"))

        self.assertEqual(self.group.booking_set.count(), 0)

    def testBookingTooEarlyGroup(self):
        booking = Booking(booker=self.booker,
                          group=self.group,
                          room=self.room,
                          date=date.today(),
                          start_time=time(7, 30, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_group.get_error_text("booking_start_time"))

        self.assertEqual(self.group.booking_set.count(), 0)

    def testBookingTooLateBooker(self):
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=date.today(),
                          start_time=time(10, 30, 0),
                          end_time=time(22, 30, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_booker.get_error_text("booking_end_time"))

        self.assertEqual(self.group.booking_set.count(), 0)

    def testBookingTooLateGroup(self):
        booking = Booking(booker=self.booker,
                          group=self.group,
                          room=self.room,
                          date=date.today(),
                          start_time=time(10, 30, 0),
                          end_time=time(23, 30, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_group.get_error_text("booking_end_time"))

        self.assertEqual(self.group.booking_set.count(), 0)

    def testBookingTooFarInFutureBooker(self):

        date_in_4_days = date.today() + timedelta(days=4)

        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=date_in_4_days,
                          start_time=time(12, 0, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_booker.get_error_text("max_days_until_booking"))

        self.assertEqual(self.booker.booking_set.count(), 0)

    def testBookingTooFarInFutureGroup(self):

        date_in_6_days = date.today() + timedelta(days=6)

        booking = Booking(booker=self.booker,
                          group=self.group,
                          room=self.room,
                          date=date_in_6_days,
                          start_time=time(12, 0, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_group.get_error_text("max_days_until_booking"))

        self.assertEqual(self.group.booking_set.count(), 0)

    def testTooManyOverallBookingsBooker(self):

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today(),
                           start_time=time(12, 0, 0),
                           end_time=time(13, 0, 0)
                           )
        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today() + datetime.timedelta(1),
                           start_time=time(13, 0, 0),
                           end_time=time(14, 0, 0)
                           )
        booking2.save()

        # Date is the same as booking2, should not be counted
        booking2_2 = Booking(booker=self.booker,
                             room=self.room,
                             date=date.today() + datetime.timedelta(1),
                             start_time=time(14, 0, 0),
                             end_time=time(16, 0, 0)
                             )
        booking2_2.save()

        booking3 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today() + datetime.timedelta(2),
                           start_time=time(14, 0, 0),
                           end_time=time(15, 0, 0)
                           )

        self.assertEqual(self.booker.booking_set.count(), 3)
        with mock_datetime(datetime.datetime(date.today().year,
                                             date.today().month,
                                             date.today().day,
                                             11, 30, 0, 0), datetime):
            try:
                booking3.save()
            except PrivilegeError as error:
                self.assertEqual(error.message, self.p_c_booker.get_error_text("max_num_days_with_bookings"))

    def testTooManyOverallBookingsGroup(self):

        booking1 = Booking(booker=self.booker,
                           group=self.group,
                           room=self.room,
                           date=date.today(),
                           start_time=time(12, 0, 0),
                           end_time=time(13, 0, 0)
                           )
        booking1.save()

        booking2 = Booking(booker=self.booker,
                           group=self.group,
                           room=self.room,
                           date=date.today() + datetime.timedelta(1),
                           start_time=time(13, 0, 0),
                           end_time=time(14, 0, 0)
                           )
        booking2.save()

        # Date is the same as booking2, should not be counted
        booking2_2 = Booking(booker=self.booker,
                             group=self.group,
                             room=self.room,
                             date=date.today() + datetime.timedelta(1),
                             start_time=time(14, 0, 0),
                             end_time=time(16, 0, 0)
                             )
        booking2_2.save()

        booking3 = Booking(booker=self.booker,
                           group=self.group,
                           room=self.room,
                           date=date.today() + datetime.timedelta(2),
                           start_time=time(13, 0, 0),
                           end_time=time(14, 0, 0)
                           )

        self.assertEqual(self.group.booking_set.count(), 3)
        with mock_datetime(datetime.datetime(date.today().year,
                                             date.today().month,
                                             date.today().day,
                                             11, 30, 0, 0), datetime):
            try:
                booking3.save()
            except PrivilegeError as error:
                self.assertEqual(error.message, self.p_c_group.get_error_text("max_num_days_with_bookings"))

    def testTooManyBookingsForDateBooker(self):

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today(),
                           start_time=time(12, 0, 0),
                           end_time=time(13, 0, 0)
                           )
        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today(),
                           start_time=time(13, 0, 0),
                           end_time=time(14, 0, 0)
                           )
        booking2.save()

        # Date is not the same as booking2, should not be counted
        booking2_2 = Booking(booker=self.booker,
                             room=self.room,
                             date=date.today() + datetime.timedelta(1),
                             start_time=time(15, 0, 0),
                             end_time=time(16, 0, 0)
                             )
        booking2_2.save()

        booking3 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today(),
                           start_time=time(14, 0, 0),
                           end_time=time(15, 0, 0)
                           )

        self.assertEqual(self.booker.booking_set.count(), 3)
        with mock_datetime(datetime.datetime(date.today().year,
                                             date.today().month,
                                             date.today().day,
                                             11, 30, 0, 0), datetime):
            try:
                booking3.save()
            except PrivilegeError as error:
                self.assertEqual(error.message, self.p_c_booker.get_error_text("max_num_bookings_for_date"))

    def testTooManyDailyBookingsGroup(self):

        booking1 = Booking(booker=self.booker,
                           group=self.group,
                           room=self.room,
                           date=date.today(),
                           start_time=time(12, 0, 0),
                           end_time=time(13, 0, 0)
                           )
        booking1.save()

        booking2 = Booking(booker=self.booker,
                           group=self.group,
                           room=self.room,
                           date=date.today(),
                           start_time=time(15, 0, 0),
                           end_time=time(16, 0, 0)
                           )
        booking2.save()

        # Date is not the same as booking2, should not be counted
        booking2_2 = Booking(booker=self.booker,
                             group=self.group,
                             room=self.room,
                             date=date.today() + datetime.timedelta(1),
                             start_time=time(15, 0, 0),
                             end_time=time(16, 0, 0)
                             )
        booking2_2.save()

        booking3 = Booking(booker=self.booker,
                           group=self.group,
                           room=self.room,
                           date=date.today(),
                           start_time=time(13, 0, 0),
                           end_time=time(14, 0, 0)
                           )

        self.assertEqual(self.group.booking_set.count(), 3)
        with mock_datetime(datetime.datetime(date.today().year,
                                             date.today().month,
                                             date.today().day,
                                             11, 30, 0, 0), datetime):
            try:
                booking3.save()
            except PrivilegeError as error:
                self.assertEqual(error.message, self.p_c_group.get_error_text("max_num_bookings_for_date"))
