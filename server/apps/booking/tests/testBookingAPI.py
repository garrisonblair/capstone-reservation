import datetime
import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
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

        booker = Booker(booker_id="j_lenn")
        booker.user = self.user
        booker.save()

        room = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        room.save()

    def testCreateBookingSuccess(self):

        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    },
                                    format="json")

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
        self.assertEqual(created_booking.booker, Booker.objects.get(booker_id='j_lenn'))

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

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-7", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.filter(date=oct7_date)
        self.assertEqual(len(bookings_oct7), 1)

        request = self.factory.get("/booking",
                                   {
                                        "year": 2018,
                                        "month": 10,
                                        "day": 7
                                    },
                                   format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 1)
        self.assertEqual(len(returned_bookings), len(bookings_oct7))

    def testViewBookingssMultipleResults(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-7", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.filter(date=oct7_date)
        self.assertEqual(len(bookings_oct7), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 7,
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 2)
        self.assertEqual(len(returned_bookings), len(bookings_oct7))

    def testViewBookingsNoResult(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)
        oct7_date = datetime.date(2019, 10, 7)
        bookings_oct7 = Booking.objects.filter(date=oct7_date)
        self.assertEqual(len(bookings_oct7), 0)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 7,
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 0)
        self.assertEqual(len(returned_bookings), len(bookings_oct7))

    def testViewBookingsNoArguements(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/booking",
                                   {
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 2)
        self.assertEqual(len(returned_bookings), len(all_bookings))

    def testViewBookingsSomeArguements(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 2)
        self.assertEqual(len(returned_bookings), len(all_bookings))

    def testViewBookingsInvalidYear(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": -1,
                                       "month": 20,
                                       "day": 7
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsInvalidMonth(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 20,
                                       "day": 7
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsInvalidDay(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 99
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsNonIntegerArgument(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/booking",
                                   {
                                       "year": "abc",
                                       "month": 10,
                                       "day": 7
                                   }, format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def editBookingSuccessful(self):

        # Setup one Booking
        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()

        # Get the added Booking
        all_bookings = Booking.objects.all()
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.filter(date=oct7_date)
        self.assertEqual(len(bookings_oct7), 1)

        request = self.factory.patch("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "16:00:00"
                                    },
                                   format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 1)
        self.assertEqual(returned_bookings.end_time, datetime.time(16, 00))

    def editBookingOverlap(self):

        # Setup one Booking
        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(room_id=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Setup second Booking
        booker2 = Booker(booker_id='87654321')
        booker2.user = None
        booker2.save()

        booking2 = Booking(booker=booker, room=room, date="2018-10-6", start_time="15:00", end_time="17:00")
        booking2.save()

        # Get the added Bookings
        all_bookings = Booking.objects.all()
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.filter(date=oct7_date)
        self.assertEqual(len(bookings_oct7), 2)

        request = self.factory.patch("/booking",
                                    {
                                        "room": 2,
                                        "date": "2018-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "16:00:00"
                                    },
                                   format="json")
        response = BookingView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
