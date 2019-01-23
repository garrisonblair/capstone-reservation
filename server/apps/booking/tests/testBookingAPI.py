import datetime
import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ContentType, ADDITION, CHANGE

from apps.accounts.models.User import User
from apps.booking.models.CampOn import CampOn
from apps.rooms.models.Room import Room
from ..models.Booking import Booking

from ..views.booking import BookingList, BookingCancel
from ..views.booking import BookingCreate
from ..views.booking import BookingRetrieveUpdateDestroy

from ..serializers.booking import BookingSerializer

from apps.util.mock_datetime import mock_datetime


class BookingAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.booker = User.objects.create_user(username='john',
                                               email='jlennon@beatles.com',
                                               password='glass onion')
        self.booker.save()

        self.booker_2 = User.objects.create_user(username="f_daigl",
                                                 email="fred@email.com",
                                                 password="passw0rd")
        self.booker_2.save()

        self.booker_3 = User.objects.create_user(username="s_loc",
                                                 email="steve@email.com",
                                                 password="passw0rd")
        self.booker_3.save()

        self.room = Room(name="H833-17", capacity=4, number_of_computers=1)
        self.room.save()

        self.datetime = datetime.datetime(2019, 1, 1, 8, 0)

    def testCreateBookingSuccess(self):

        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": self.datetime.date(),
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    },
                                    format="json")

        force_authenticate(request, user=self.booker)

        with mock_datetime(self.datetime, datetime):
            response = BookingCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bookings = Booking.objects.all()
        self.assertEqual(len(bookings), 1)
        created_booking = bookings[0]
        self.assertEqual(created_booking.start_time, datetime.time(14, 0))
        self.assertEqual(created_booking.end_time, datetime.time(15, 0))
        self.assertEqual(created_booking.date, self.datetime.date())
        self.assertEqual(created_booking.room, Room.objects.get(name="H833-17"))
        self.assertEqual(created_booking.booker, self.booker)

        # LogEntry test
        latest_booking_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_booking_log.action_flag, ADDITION)
        self.assertEqual(latest_booking_log.object_id, str(created_booking.id))
        self.assertEqual(latest_booking_log.user, self.booker)
        self.assertEqual(latest_booking_log.object_repr, json.dumps(BookingSerializer(created_booking).data))

    def testCreateBookingNotAuthenticated(self):
        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": self.datetime.date(),
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        with mock_datetime(self.datetime, datetime):
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

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="16:00", end_time="17:00")
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

    def testViewBookingsMultipleResults(self):

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="16:00", end_time="17:00")
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

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=self.booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
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

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=self.booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
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

        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-6", start_time="14:00", end_time="15:00")
        booking1.save()
        booking2 = Booking(booker=self.booker, room=room, date="2018-10-8", start_time="16:00", end_time="17:00")
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

        with mock_datetime(datetime.datetime(2018, 10, 6, 12, 30, 0, 0), datetime):
            response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Booking.objects.all()), 1)
        edit_booking = Booking.objects.last()
        self.assertEqual(edit_booking.end_time, datetime.time(16, 00))

        # LogEntry test
        latest_booking_log = LogEntry.objects.last()  # type: LogEntry
        self.assertEqual(latest_booking_log.action_flag, CHANGE)
        self.assertEqual(latest_booking_log.object_id, str(edit_booking.id))
        self.assertEqual(latest_booking_log.user, self.booker)
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
        with mock_datetime(datetime.datetime(2018, 10, 6, 12, 30, 0, 0), datetime):
            response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Booking.objects.all()), 1)
        edit_booking = Booking.objects.last()
        self.assertEqual(edit_booking.booker, self.booker)

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
        force_authenticate(request, user=user1)
        with mock_datetime(datetime.datetime(2018, 10, 6, 12, 30, 0, 0), datetime):
            response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testEditBookingOverlapEndTime(self):

        # Setup one Booking
        room = Room(name=2, capacity=4, number_of_computers=1)
        room.save()

        booking1 = Booking(booker=self.booker, room=room, date="2018-10-7", start_time="14:00", end_time="15:00")
        booking1.save()

        # Setup second Booking
        # Setup another booker
        booker2 = User.objects.create_user(username='solji',
                                           email='solji@exid.com',
                                           password='maskOfKing')
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
        with mock_datetime(datetime.datetime(2018, 10, 6, 12, 30, 0, 0), datetime):
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
        # Setup another booker
        booker2 = User.objects.create_user(username='solji',
                                           email='solji@exid.com',
                                           password='maskOfKing')
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

        with mock_datetime(datetime.datetime(2018, 10, 6, 12, 30, 0, 0), datetime):
            response = BookingRetrieveUpdateDestroy.as_view()(request, 1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(Booking.objects.all()), 2)

    def testEditBookingAfterStart(self):
        booking = Booking(booker=self.booker, room=self.room, date="2018-10-7", start_time="13:00", end_time="15:00")
        booking.save()

        request = self.factory.patch("/booking", {
                                        "start_time": "14:00:00"
                                    }, format="json")
        force_authenticate(request, user=self.booker)

        with mock_datetime(datetime.datetime(2018, 10, 7, 13, 1, 0, 0), datetime):
            response = BookingRetrieveUpdateDestroy.as_view()(request, booking.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testCancelBookingNotAuthenticated(self):
        booking = Booking(booker=self.booker, room=self.room, date="2018-10-7", start_time="13:00", end_time="15:00")
        booking.save()

        bookings_before_cancel = len(Booking.objects.all())

        request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
        }, format="json")
        response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel)

    def testCancelBookingNonExistentBooking(self):
        booking = Booking(booker=self.booker, room=self.room, date="2019-10-7", start_time="13:00", end_time="15:00")
        booking.save()

        bookings_before_cancel = len(Booking.objects.all())

        request = self.factory.post("/booking/" + str(-99999) + "/cancel_booking", {
        }, format="json")
        force_authenticate(request, user=self.booker)
        response = BookingCancel.as_view()(request, -99999)

        bookings_after_cancel = len(Booking.objects.all())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel)

    def testCancelBookingAfterBookingEnded(self):
        booking = Booking(booker=self.booker, room=self.room, date="2018-10-7", start_time="13:00", end_time="15:00")
        booking.save()

        bookings_before_cancel = len(Booking.objects.all())

        request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
                                    }, format="json")
        force_authenticate(request, user=self.booker)
        response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel)

    def testCancelBookingNoCamponsSuccess(self):
        booking = Booking(booker=self.booker, room=self.room, date="2019-10-7", start_time="13:00", end_time="15:00")
        booking.save()

        bookings_before_cancel = len(Booking.objects.all())

        request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
                                    }, format="json")
        force_authenticate(request, user=self.booker)
        response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel+1)

    def testCancelBookingOneCamponSuccess(self):

        today = datetime.datetime.now().date()

        booking = Booking(booker=self.booker, room=self.room, date=today, start_time="10:00", end_time="23:00")
        booking.save()

        campon = CampOn(booker=self.booker_2,
                        camped_on_booking=booking,
                        start_time=booking.start_time,
                        end_time=booking.end_time)
        campon.save()

        bookings_before_cancel = len(Booking.objects.all())
        campons_before_cancel = len(CampOn.objects.all())

        request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
                                    }, format="json")
        force_authenticate(request, user=self.booker)
        response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())
        campons_after_cancel = len(CampOn.objects.all())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel)
        self.assertEqual(campons_before_cancel, campons_after_cancel+1)

    def testCancelBookingMultipleCamponsSameEndTimeSuccess(self):

        today = datetime.datetime.now().date()

        booking = Booking(booker=self.booker, room=self.room, date=today, start_time="10:00", end_time="23:00")
        booking.save()

        campon = CampOn(booker=self.booker_2,
                        camped_on_booking=booking,
                        start_time=booking.start_time,
                        end_time=booking.end_time)
        campon.save()

        campon2 = CampOn(booker=self.booker_3,
                         camped_on_booking=booking,
                         start_time=booking.start_time,
                         end_time=booking.end_time)
        campon2.save()

        bookings_before_cancel = len(Booking.objects.all())
        campons_before_cancel = len(CampOn.objects.all())

        request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
                                    }, format="json")
        force_authenticate(request, user=self.booker)
        response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())
        campons_after_cancel = len(CampOn.objects.all())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel)
        self.assertEqual(campons_before_cancel, campons_after_cancel+1)

    def testCancelBookingMultipleCamponsFirstEndsBeforeSecondSuccess(self):

        today = datetime.datetime.now().date()

        booking = Booking(booker=self.booker, room=self.room, date=today, start_time="10:00", end_time="22:00")
        booking.save()

        campon = CampOn(booker=self.booker_2,
                        camped_on_booking=booking,
                        start_time=datetime.time(10, 0),
                        end_time=datetime.time(20, 0))
        campon.save()

        campon2 = CampOn(booker=self.booker_3,
                         camped_on_booking=booking,
                         start_time=datetime.time(10, 0),
                         end_time=datetime.time(22, 0))
        campon2.save()

        bookings_before_cancel = len(Booking.objects.all())

        with mock_datetime(datetime.datetime(today.year, today.month, today.day, 11, 30, 0, 0), datetime):
            request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
                                        }, format="json")
            force_authenticate(request, user=self.booker)
            response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bookings_after_cancel, bookings_before_cancel+1)

    def testCancelBookingMultipleCamponsSecondEndsBeforeFirstSuccess(self):

        today = datetime.datetime.now().date()

        booking = Booking(booker=self.booker, room=self.room, date=today, start_time="00:00", end_time="23:59")
        booking.save()

        campon = CampOn(booker=self.booker_2,
                        camped_on_booking=booking,
                        start_time=datetime.time(10, 0),
                        end_time=datetime.time(22, 0))
        campon.save()

        campon2 = CampOn(booker=self.booker_3,
                         camped_on_booking=booking,
                         start_time=datetime.time(10, 0),
                         end_time=datetime.time(20, 0))
        campon2.save()

        bookings_before_cancel = len(Booking.objects.all())
        with mock_datetime(datetime.datetime(today.year, today.month, today.day, 11, 30, 0, 0), datetime):
            request = self.factory.post("/booking/" + str(booking.id) + "/cancel_booking", {
                                        }, format="json")

            force_authenticate(request, user=self.booker)
            response = BookingCancel.as_view()(request, booking.id)

        bookings_after_cancel = len(Booking.objects.all())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bookings_before_cancel, bookings_after_cancel)
