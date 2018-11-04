from django.test import TestCase
from datetime import date, time, timedelta

from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from ..models.Booking import Booking
from apps.groups.models.StudentGroup import StudentGroup
from apps.accounts.exceptions import PrivilegeError


class TestBookingPrivileges(TestCase):

    def setUp(self):
        self.p_c_booker = PrivilegeCategory(name="Booker Category")

        self.p_c_booker.num_days_to_booking = 3
        self.p_c_booker.max_num_bookings = 2
        self.p_c_booker.save()

        self.booker = Booker(booker_id="11111111", privilege_category=self.p_c_booker)
        self.booker.save()

        self.p_c_group = PrivilegeCategory(name="Group Category")
        self.p_c_group.num_days_to_booking = 5
        self.p_c_group.max_num_bookings = 1
        self.p_c_group.save()

        self.group = StudentGroup(name="Group 1",
                                  is_verified=True,
                                  privilege_category=self.p_c_group)
        self.group.save()
        self.group.students.add(self.booker)
        self.group.save()

        self.room = Room(room_id="H916-01")
        self.room.save()

    def testBookingAllowedBooker(self):

        date_in_3_days = date.today() + timedelta(days=3)

        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=date_in_3_days,
                          start_time=time(12, 0, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError:
            self.fail("Booking should be saved.")
            return

        self.assertTrue(True)

    def testBookingAllowedGroup(self):

        date_in_5_days = date.today() + timedelta(days=5)

        booking = Booking(booker=self.booker,
                          student_group=self.group,
                          room=self.room,
                          date=date_in_5_days,
                          start_time=time(12, 0, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError:
            self.fail("Booking should be saved.")
            return

        self.assertTrue(True)

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
            self.assertEqual(error.message, self.p_c_booker.get_error_text("num_days_to_booking"))

        self.assertEqual(len(Booking.objects.all()), 0)

    def testBookingTooFarInFutureGroup(self):

        date_in_6_days = date.today() + timedelta(days=6)

        booking = Booking(booker=self.booker,
                          student_group=self.group,
                          room=self.room,
                          date=date_in_6_days,
                          start_time=time(12, 0, 0),
                          end_time=time(13, 0, 0)
                          )

        try:
            booking.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_booker.get_error_text("num_days_to_booking"))

        self.assertEqual(len(Booking.objects.all()), 0)

    def testTooManyBookingsBooker(self):

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

        booking3 = Booking(booker=self.booker,
                           room=self.room,
                           date=date.today(),
                           start_time=time(14, 0, 0),
                           end_time=time(15, 0, 0)
                           )

        try:
            booking3.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_booker.get_error_text("max_num_bookings"))

        self.assertEqual(len(Booking.objects.all()), 2)

    def testTooManyBookingsGroup(self):

        booking1 = Booking(booker=self.booker,
                           student_group=self.group,
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

        try:
            booking2.save()
        except PrivilegeError as error:
            self.assertEqual(error.message, self.p_c_booker.get_error_text("max_num_bookings"))

        self.assertEqual(len(Booking.objects.all()), 1)
