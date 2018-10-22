from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import timedelta

from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.Booking import Booking
from apps.accounts.models.Student import Student
from apps.groups.models.StudentGroup import StudentGroup
from apps.rooms.models.Room import Room
from datetime import datetime


class TestRecurringBooking(TestCase):
    def setUp(self):
        # Create 2 students
        sid = '00000001'
        student1 = Student(student_id=sid)
        student1.user = None
        student1.save()

        sid = '00000002'
        student2 = Student(student_id=sid)
        student2.user = None
        student2.save()

        # Create student group
        name = "Students group"
        self.group = StudentGroup(name=name, is_verified=True)
        self.group.save()
        self.group.students.add(student1)
        self.group.students.add(student2)

        # Create room
        rid = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(room_id=rid, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        # Create date and times
        start = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end = datetime.strptime("2019-10-16 15:00", "%Y-%m-%d %H:%M")
        self.start_date = start.date()
        self.end_date = end.date()
        self.start_time = start.time()
        self.end_time = end.time()

    def testRecurringBookingCreation(self):
        recurring_booking = RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.group.students.get(student_id='00000001'),
            False
        )
        self.assertEqual(recurring_booking.booking_set.count(), 3)

        recurring_booking = RecurringBooking.objects.get(start_date=self.start_date)
        booking1 = recurring_booking.booking_set.get(date=self.start_date)

        self.assertEqual(booking1.start_time, self.start_time)
        self.assertEqual(booking1.end_time, self.end_time)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.student_group, self.group)
        self.assertEqual(booking1.student, self.group.students.get(student_id='00000001'))

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.student_group, self.group)
        self.assertEqual(booking2.student, self.group.students.get(student_id='00000001'))

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.student_group, self.group)
        self.assertEqual(booking3.student, self.group.students.get(student_id='00000001'))

    def testRecurringBookingCreationConflict(self):
        RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.group.students.get(student_id='00000001'),
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
                self.group.students.get(student_id='00000001'),
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
                self.group.students.get(student_id='00000001'),
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
                self.group.students.get(student_id='00000001'),
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
                self.group.students.get(student_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 0)

    def testRecurringBookingSingleConflictFlagNotSet(self):
        Booking(
            student=self.group.students.get(student_id='00000001'),
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
                self.group.students.get(student_id='00000001'),
                False
            )
        self.assertEqual(RecurringBooking.objects.count(), 0)

    def testRecurringBookingSingleConflictFlagSet(self):
        Booking(
            student=self.group.students.get(student_id='00000001'),
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
            self.group.students.get(student_id='00000001'),
            True
        )
        self.assertEqual(RecurringBooking.objects.count(), 1)

        # In the first week the booking should not be made, but will be made the following weeks
        recurring_booking = RecurringBooking.objects.get(student_group=self.group)
        self.assertEqual(recurring_booking.booking_set.count(), 2)

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.student_group, self.group)
        self.assertEqual(booking2.student, self.group.students.get(student_id='00000001'))

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.student_group, self.group)
        self.assertEqual(booking3.student, self.group.students.get(student_id='00000001'))
