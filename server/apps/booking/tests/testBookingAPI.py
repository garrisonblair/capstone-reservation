import datetime
import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from ..models.Booking import Booking

from ..views.booking import BookingView


class BookingAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        self.user.save()

        student = Student(student_id="j_lenn")
        student.user = self.user
        student.save()

        room = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        room.save()

    def testCreateBookingSuccess(self):

        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 1)
        created_booking = bookings[0]
        self.assertEqual(created_booking.start_time, datetime.time(14, 0))
        self.assertEqual(created_booking.end_time, datetime.time(15, 0))
        self.assertEqual(created_booking.date, datetime.date(2019, 8, 10))
        self.assertEqual(created_booking.room, Room.objects.get(room_id="H833-17"))
        self.assertEqual(created_booking.student, Student.objects.get(student_id='j_lenn'))

    def testCreateBookingNotAuthenticated(self):
        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testCreateBookingInvalidPayload(self):
        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019/08/10",  # Wrong Date Format
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsOneResult(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-7", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)
        oct7Date = datetime.date(2018, 10, 7)
        bookingsOct7 = Booking.objects.filter(date=oct7Date)
        self.assertEqual(len(bookingsOct7), 1)

        request = self.factory.get("/booking",
                                    {
                                        "year": 2018,
                                        "month": 10,
                                        "day": 7
                                    }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returnedBookings = response.data
        self.assertEqual(len(returnedBookings), 1)
        self.assertEqual(len(returnedBookings), len(bookingsOct7))


    def testViewBookingssMultipleResults(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-7", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-7", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)
        oct7Date = datetime.date(2018, 10, 7)
        bookingsOct7 = Booking.objects.filter(date=oct7Date)
        self.assertEqual(len(bookingsOct7), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 7,
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returnedBookings = response.data
        self.assertEqual(len(returnedBookings), 2)
        self.assertEqual(len(returnedBookings), len(bookingsOct7))


    def testViewBookingsNoResult(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)
        oct7Date = datetime.date(2019, 10, 7)
        bookingsOct7 = Booking.objects.filter(date=oct7Date)
        self.assertEqual(len(bookingsOct7), 0)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 7,
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returnedBookings = response.data
        self.assertEqual(len(returnedBookings), 0)
        self.assertEqual(len(returnedBookings), len(bookingsOct7))


    def testViewBookingsNoArguements(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)

        request = self.factory.get("/booking",
                                   {
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returnedBookings = response.data
        self.assertEqual(len(returnedBookings), 2)
        self.assertEqual(len(returnedBookings), len(allBookings))

    def testViewBookingsSomeArguements(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returnedBookings = response.data
        self.assertEqual(len(returnedBookings), 2)
        self.assertEqual(len(returnedBookings), len(allBookings))


    def testViewBookingsInvalidYear(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": -1,
                                       "month": 20,
                                       "day": 7
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsInvalidMonth(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 20,
                                       "day": 7
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsInvalidDay(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 99
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsNonIntegerArgument(self):

        student = Student(student_id='12345678')
        student.user = None
        student.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(student=student, room=room, date="2018-10-6", start_time="14:00:00", end_time="15:00:00")
        booking1.save()
        booking2 = Booking(student=student, room=room, date="2018-10-8", start_time="16:00:00", end_time="17:00:00")
        booking2.save()

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": "abc",
                                       "month": 10,
                                       "day": 7
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
