import datetime
import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ContentType, ADDITION, CHANGE

from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from ..models.Booking import Booking

from ..views.booking import BookingList
from ..views.booking import BookingCreate
from ..views.booking import BookingRetrieveUpdateDestroy

from ..serializers.booking import BookingSerializer


class BookingAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        self.booker = Booker(booker_id="j_lenn")
        self.booker.user = self.user
        self.booker.save()

        room = Room(name="H833-17", capacity=4, number_of_computers=1)
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

        force_authenticate(request, user=self.user)

        response = BookingCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 1)
        created_booking = bookings[0]
        self.assertEqual(created_booking.start_time, datetime.time(14, 0))
        self.assertEqual(created_booking.end_time, datetime.time(15, 0))
        self.assertEqual(created_booking.date, datetime.date(2019, 8, 10))
        self.assertEqual(created_booking.room, Room.objects.get(name="H833-17"))
        self.assertEqual(created_booking.booker, Booker.objects.get(booker_id='j_lenn'))

        # LogEntry test
        latest_booking_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_booking_log.action_flag, ADDITION)
        self.assertEqual(latest_booking_log.object_id, str(created_booking.id))
        self.assertEqual(latest_booking_log.user, self.user)
        self.assertEqual(latest_booking_log.object_repr, json.dumps(BookingSerializer(created_booking).data))

    def testCreateBookingNotAuthenticated(self):
        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        response = BookingRetrieveUpdateDestroy.as_view()(request)

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

        response = BookingCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testViewBookingsOneResult(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(name=2, capacity=4, number_of_computers=1)
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

        request = self.factory.get("/bookings",
                                   {
                                        "year": 2018,
                                        "month": 10,
                                        "day": 7
                                    },
                                   format="json")
        response = BookingList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 1)
        self.assertEqual(len(returned_bookings), len(bookings_oct7))

    def testViewBookingssMultipleResults(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(name=2, capacity=4, number_of_computers=1)
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

        params = {
            "year": 2018,
            "month": 10,
            "day": 7,
        }

        request = self.factory.get("/bookings", params, format="json")
        response = BookingList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 2)
        self.assertEqual(len(returned_bookings), len(bookings_oct7))

    def testViewBookingsNoResult(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(name=2, capacity=4, number_of_computers=1)
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

        request = self.factory.get("/bookings",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                       "day": 7,
                                   }, format="json")
        response = BookingList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 0)
        self.assertEqual(len(returned_bookings), len(bookings_oct7))

    def testViewBookingsNoArguments(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/bookings", format="json")
        response = BookingList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 2)
        self.assertEqual(len(returned_bookings), len(all_bookings))

    def testViewBookingsSomeArguments(self):

        booker = Booker(booker_id='12345678')
        booker.user = None
        booker.save()

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
        booking2.save()

        all_bookings = Booking.objects.all()
        self.assertEqual(len(all_bookings), 2)

        request = self.factory.get("/bookings",
                                   {
                                       "year": 2018,
                                       "month": 10,
                                   }, format="json")
        response = BookingList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_bookings = response.data
        self.assertEqual(len(returned_bookings), 2)
        self.assertEqual(len(returned_bookings), len(all_bookings))

    def testEditBookingSuccessful(self):

        # Setup one Booking
        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Get the added Booking
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.last()
        request = self.factory.patch("/booking", {
                                        "room": 2,
                                        "date": "2018-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "16:00:00"
                                    },
                                   format="json")
        force_authenticate(request, user=User.objects.get(username="john"))
        response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Booking.objects.all()), 1)
        edit_booking = Booking.objects.last()
        self.assertEqual(edit_booking.end_time, datetime.time(16, 00))

        # LogEntry test
        latest_booking_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_booking_log.action_flag, CHANGE)
        self.assertEqual(latest_booking_log.object_id, str(edit_booking.id))
        self.assertEqual(latest_booking_log.user, self.user)
        self.assertEqual(latest_booking_log.object_repr, json.dumps(BookingSerializer(edit_booking).data))

    def testEditBookingWithBookerId(self):

        # Setup one Booking
        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Get the added Booking
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.last()
        request = self.factory.patch("/booking", {
                                        "booker": "44444444",
                                        "room": 2,
                                        "date": "2018-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "16:00:00"
                                    },
                                   format="json")
        force_authenticate(request, user=User.objects.get(username="john"))
        response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Booking.objects.all()), 1)
        edit_booking = Booking.objects.last()
        self.assertEqual(edit_booking.booker.booker_id, "j_lenn")

    def testEditBookingForbidden(self):

        # Setup one Booking
        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Setup another booker
        user1 = User.objects.create_user(username='solji',
                                         email='solji@exid.com',
                                         password='maskOfKing')
        user1.save()

        booker1 = Booker(booker_id="sol_exid")
        booker1.user = user1
        booker1.save()

        # Get the added Booking
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.last()
        request = self.factory.patch("/booking", {
                                        "room": 2,
                                        "date": "2018-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "16:00:00"
                                    },
                                   format="json")
        force_authenticate(request, user=User.objects.get(username="solji"))
        response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testEditBookingOverlapEndTime(self):

        # Setup one Booking
        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Setup second Booking
        booker2 = Booker(booker_id='87654321')
        booker2.user = None
        booker2.save()

        booking2 = Booking(booker=booker2, room=room, date="2018-10-7", start_time="15:00", end_time="17:00")
        booking2.save()

        # Get the added Booking
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.last()
        request = self.factory.patch("/booking", {
                                        "room": 2,
                                        "date": "2018-10-7",
                                        "start_time": "14:00:00",
                                        "end_time": "16:00:00"
                                    },
                                   format="json")
        force_authenticate(request, user=User.objects.get(username="john"))
        response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(Booking.objects.all()), 2)

    def testEditBookingOverlapStartTime(self):

        # Setup one Booking
        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Setup second Booking
        booker2 = Booker(booker_id='87654321')
        booker2.user = None
        booker2.save()

        booking2 = Booking(booker=booker2, room=room, date="2018-10-7", start_time="13:00", end_time="14:00")
        booking2.save()

        # Get the added Booking
        oct7_date = datetime.date(2018, 10, 7)
        bookings_oct7 = Booking.objects.last()
        request = self.factory.patch("/booking", {
                                        "room": 2,
                                        "date": "2018-10-7",
                                        "start_time": "13:30:00",
                                        "end_time": "15:00:00"
                                    },
                                   format="json")
        force_authenticate(request, user=User.objects.get(username="john"))
        response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(Booking.objects.all()), 2)
