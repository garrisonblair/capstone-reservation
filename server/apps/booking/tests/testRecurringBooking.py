from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import timedelta

from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.Booking import Booking
from apps.accounts.models.Booker import Booker
from apps.groups.models.Group import Group
from apps.rooms.models.Room import Room
from datetime import datetime


class TestRecurringBooking(TestCase):
    def setUp(self):
        # Create 2 bookers
        sid = '00000001'
        booker1 = Booker(booker_id=sid)
        booker1.user = None
        booker1.save()

        sid = '00000002'
        booker2 = Booker(booker_id=sid)
        booker2.user = None
        booker2.save()

        # Create student group
        name = "Students group"
        self.group = Group(name=name, is_verified=True)
        self.group.save()
        self.group.bookers.add(booker1)
        self.group.bookers.add(booker2)

        # Create room
        name = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        # Create date and times
        start = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end = datetime.strptime("2019-10-16 15:00", "%Y-%m-%d %H:%M")
        self.start_date = start.date()
        self.end_date = end.date()
        self.start_time = start.time()
        self.end_time = end.time()

    def testRecurringBookingCreation(self):
        recurring_booking, conflicts = RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.group.bookers.get(booker_id='00000001'),
            False
        )
        self.assertEqual(recurring_booking.booking_set.count(), 3)

        recurring_booking = RecurringBooking.objects.get(start_date=self.start_date)
        booking1 = recurring_booking.booking_set.get(date=self.start_date)

        self.assertEqual(booking1.start_time, self.start_time)
        self.assertEqual(booking1.end_time, self.end_time)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.group, self.group)
        self.assertEqual(booking1.booker, self.group.bookers.get(booker_id='00000001'))

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.group, self.group)
        self.assertEqual(booking2.booker, self.group.bookers.get(booker_id='00000001'))

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.group, self.group)
        self.assertEqual(booking3.booker, self.group.bookers.get(booker_id='00000001'))

    def testRecurringBookingCreationConflict(self):
        RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.group.bookers.get(booker_id='00000001'),
            False
        )
        with self.assertRaises(ValidationError):
            RecurringBooking.objects.create_recurring_booking(
                self.start_date,
                self.end_date,
                self.start_time,
                self.end_time,
                self.room,
                self.group,
                self.group.bookers.get(booker_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 1)

    def testRecurringBookingWrongDateOrder(self):
        with self.assertRaises(ValidationError):
            RecurringBooking.objects.create_recurring_booking(
                self.end_date,
                self.start_date,
                self.start_time,
                self.end_time,
                self.room,
                self.group,
                self.group.bookers.get(booker_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 0)

    def testRecurringBookingWrongTimeOrder(self):
        with self.assertRaises(ValidationError):
            RecurringBooking.objects.create_recurring_booking(
                self.start_date,
                self.end_date,
                self.end_time,
                self.start_time,
                self.room,
                self.group,
                self.group.bookers.get(booker_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 0)

    def testRecurringBookingGroupNotVerified(self):
        self.group.is_verified = False
        with self.assertRaises(ValidationError):
            RecurringBooking.objects.create_recurring_booking(
                self.start_date,
                self.end_date,
                self.end_time,
                self.start_time,
                self.room,
                self.group,
                self.group.bookers.get(booker_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 0)

    def testRecurringBookingSingleConflictFlagNotSet(self):
        Booking(
            booker=self.group.bookers.get(booker_id='00000001'),
            room=self.room,
            date=self.start_date,
            start_time=self.start_time,
            end_time=self.end_time
        ).save()

        with self.assertRaises(ValidationError):
            RecurringBooking.objects.create_recurring_booking(
                self.start_date,
                self.end_date,
                self.start_time,
                self.end_time,
                self.room,
                self.group,
                self.group.bookers.get(booker_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 0)

    def testRecurringBookingSingleConflictFlagSet(self):
        Booking(
            booker=self.group.bookers.get(booker_id='00000001'),
            room=self.room,
            date=self.start_date,
            start_time=self.start_time,
            end_time=self.end_time
        ).save()

        RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.group.bookers.get(booker_id='00000001'),
            True
        )
        self.assertEqual(RecurringBooking.objects.count(), 1)

        # In the first week the booking should not be made, but will be made the following weeks
        recurring_booking = RecurringBooking.objects.get(group=self.group)
        self.assertEqual(recurring_booking.booking_set.count(), 2)

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.group, self.group)
        self.assertEqual(booking2.booker, self.group.bookers.get(booker_id='00000001'))

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.group, self.group)
        self.assertEqual(booking3.booker, self.group.bookers.get(booker_id='00000001'))
