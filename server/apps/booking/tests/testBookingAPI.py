import datetime

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

    def testViewRoomsOneResult(self):
        requestRoom1 = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")

        force_authenticate(requestRoom1, user=User.objects.get(username="john"))
        responseRoom1 = BookingView.as_view()(requestRoom1)
        self.assertEqual(responseRoom1.status_code, status.HTTP_201_CREATED)


        requestRoom2 = self.factory.post("/booking",
                                    {
                                        "room": 2,
                                        "date": "2019-10-8",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        force_authenticate(requestRoom2, user=User.objects.get(username="john"))
        responseRoom2 = BookingView.as_view()(requestRoom2)
        self.assertEqual(responseRoom2.status_code, status.HTTP_201_CREATED)

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)
        oct7Date = datetime.date(2019, 10, 7)
        bookingsOct7 = Booking.objects.filter(date=oct7Date)
        self.assertEqual(len(bookingsOct7), 1)


    def testViewRoomsMultipleResults(self):
        requestRoom1 = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        force_authenticate(requestRoom1, user=User.objects.get(username="john"))
        responseRoom1 = BookingView.as_view()(requestRoom1)
        self.assertEqual(responseRoom1.status_code, status.HTTP_201_CREATED)

        requestRoom2 = self.factory.post("/booking",
                                    {
                                        "room": 2,
                                        "date": "2019-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        force_authenticate(requestRoom2, user=User.objects.get(username="john"))
        responseRoom2 = BookingView.as_view()(requestRoom2)
        self.assertEqual(responseRoom2.status_code, status.HTTP_201_CREATED)

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)
        oct7Date = datetime.date(2019, 10, 7)
        bookingsOct7 = Booking.objects.filter(date=oct7Date)
        self.assertEqual(len(bookingsOct7), 2)

    def testViewRoomNoResult(self):
        requestRoom1 = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-10-6",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        force_authenticate(requestRoom1, user=User.objects.get(username="john"))
        responseRoom1 = BookingView.as_view()(requestRoom1)
        self.assertEqual(responseRoom1.status_code, status.HTTP_201_CREATED)

        requestRoom2 = self.factory.post("/booking",
                                    {
                                        "room": 2,
                                        "date": "2019-10-6",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        force_authenticate(requestRoom2, user=User.objects.get(username="john"))
        responseRoom2 = BookingView.as_view()(requestRoom2)
        self.assertEqual(responseRoom2.status_code, status.HTTP_201_CREATED)

        allBookings = Booking.objects.all()
        self.assertEqual(len(allBookings), 2)
        oct7Date = datetime.date(2019, 10, 7)
        bookingsOct7 = Booking.objects.filter(date=oct7Date)
        self.assertEqual(len(bookingsOct7), 0)



