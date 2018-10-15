from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from datetime import timedelta, datetime

from apps.accounts.models.Student import Student
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.groups.models import StudentGroup
from apps.rooms.models.Room import Room

from ..views.recurring_booking import RecurringBookingView


class BookingAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        student1 = Student(student_id="j_lenn")
        student1.user = self.user
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

        self.room = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        self.room.save()

        start = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end = datetime.strptime("2019-10-16 15:00", "%Y-%m-%d %H:%M")
        self.start_date = start.date()
        self.end_date = end.date()
        self.start_time = start.time()
        self.end_time = end.time()

    def testCreateRecurringBookingSuccess(self):

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-01",
                                        "end_date": "2019-10-16",
                                        "booking_start_time": "12:00",
                                        "booking_end_time": "15:00",
                                        "room": 1,
                                        "student_group": 1,
                                        "student": 1
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recurring_booking = RecurringBooking.objects.get(start_date=self.start_date)
        booking1 = recurring_booking.booking_set.get(date=self.start_date)

        self.assertEqual(booking1.start_time, self.start_time)
        self.assertEqual(booking1.end_time, self.end_time)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.student_group, self.group)
        self.assertEqual(booking1.student, self.group.students.get(student_id='j_lenn'))

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.student_group, self.group)
        self.assertEqual(booking2.student, self.group.students.get(student_id='j_lenn'))

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.student_group, self.group)
        self.assertEqual(booking3.student, self.group.students.get(student_id='j_lenn'))

    def testCreateRecurringBookingFailureDateStartAfterEnd(self):

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-16",
                                        "end_date": "2019-10-01",
                                        "booking_start_time": "12:00",
                                        "booking_end_time": "15:00",
                                        "room": 1,
                                        "student_group": 1,
                                        "student": 1
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateRecurringBookingFailureTimeStartAfterEnd(self):

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-01",
                                        "end_date": "2019-10-16",
                                        "booking_start_time": "15:00",
                                        "booking_end_time": "12:00",
                                        "room": 1,
                                        "student_group": 1,
                                        "student": 1
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
