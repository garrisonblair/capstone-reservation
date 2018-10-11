from django.test import TestCase
from apps.booking.models.RecurringBooking import RecurringBooking
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
            self.group
        )

        self.assertEqual(recurring_booking.booking_set.count(), 3)
