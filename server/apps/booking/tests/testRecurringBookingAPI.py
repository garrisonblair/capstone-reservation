import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ContentType, ADDITION
import datetime

from apps.accounts.models.User import User
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.Booking import Booking
from apps.groups.models.Group import Group
from apps.rooms.models.Room import Room

from apps.booking.views.recurring_booking import RecurringBookingCreate, RecurringBookingCancel

from apps.booking.serializers.recurring_booking import LogRecurringBookingSerializer
from apps.booking.serializers.booking import LogBookingSerializer
from apps.util.mock_datetime import mock_datetime


class BookingAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create_user(username='john',
                                              email='jlennon@beatles.com',
                                              password='glass onion')
        self.user1.save()

        self.user2 = User.objects.create_user(username="f_daigl",
                                              email="fred@email.com",
                                              password="safe_password")
        self.user2.save()

        # Create student group
        name = "Students group"
        self.group = Group(name=name, is_verified=True, owner=self.user1)
        self.group.save()
        self.group.members.add(self.user1)
        self.group.members.add(self.user2)

        self.room = Room(name="H833-17", capacity=4, number_of_computers=1)
        self.room.save()

        self.room2 = Room(name="H833-18", capacity=4, number_of_computers=1)
        self.room2.save()

        start = datetime.datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end = datetime.datetime.strptime("2019-10-16 15:00", "%Y-%m-%d %H:%M")
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
                                        "group": 1,
                                        "student": 1,
                                        "skip_conflicts": False
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recurring_booking = RecurringBooking.objects.get(start_date=self.start_date)
        booking1 = recurring_booking.booking_set.get(date=self.start_date)

        self.assertEqual(booking1.start_time, self.start_time)
        self.assertEqual(booking1.end_time, self.end_time)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.group, self.group)
        self.assertEqual(booking1.booker, self.user1)

        booking2 = recurring_booking.booking_set.get(date=self.start_date + datetime.timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.group, self.group)
        self.assertEqual(booking2.booker, self.user1)

        booking3 = recurring_booking.booking_set.get(date=self.start_date + datetime.timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.group, self.group)
        self.assertEqual(booking3.booker, self.user1)

        # LogEntry test
        all_recurring_booking_logs = LogEntry.objects.all()
        latest_recurring_booking_log = all_recurring_booking_logs.order_by('action_time')[0]
        self.assertEqual(latest_recurring_booking_log.action_flag, ADDITION)
        self.assertEqual(latest_recurring_booking_log.object_id, str(recurring_booking.id))
        self.assertEqual(latest_recurring_booking_log.user, self.user1)
        self.assertEqual(latest_recurring_booking_log.change_message,
                         json.dumps(LogRecurringBookingSerializer(recurring_booking).data))

        for booking in recurring_booking.booking_set.all():
            booking_logs = LogEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(booking),
                object_id=str(booking.id))
            latest_booking_log = booking_logs.order_by('action_time')[0]

            self.assertEqual(latest_booking_log.action_flag, ADDITION)
            self.assertEqual(latest_booking_log.object_id, str(booking.id))
            self.assertEqual(latest_booking_log.user, self.user1)
            self.assertEqual(latest_booking_log.change_message,
                             json.dumps(LogBookingSerializer(booking).data))

    def testCreateRecurringBookingFailureDateStartAfterEnd(self):

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-16",
                                        "end_date": "2019-10-01",
                                        "booking_start_time": "12:00",
                                        "booking_end_time": "15:00",
                                        "room": 1,
                                        "group": 1,
                                        "student": 1,
                                        "skip_conflicts": False
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateRecurringBookingFailureTimeStartAfterEnd(self):

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-01",
                                        "end_date": "2019-10-16",
                                        "booking_start_time": "15:00",
                                        "booking_end_time": "12:00",
                                        "room": 1,
                                        "group": 1,
                                        "student": 1,
                                        "skip_conflicts": False
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateRecurringBookingFailureInvalidPayload(self):

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019/10/01",
                                        "end_date": "2019/10/16",
                                        "booking_start_time": "15:00",
                                        "booking_end_time": "12:00",
                                        "room": 1,
                                        "group": 1,
                                        "student": 1,
                                        "skip_conflicts": False
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateRecurringBookingNotAuthenticated(self):
        request = self.factory.post("/booking",
                                    {
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    }, format="json")
        response = RecurringBookingCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testRecurringBookingConflictFlagNotSet(self):
        Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=self.start_time,
            end_time=self.end_time
        ).save()

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-01",
                                        "end_date": "2019-10-16",
                                        "booking_start_time": "12:00",
                                        "booking_end_time": "15:00",
                                        "room": 1,
                                        "group": 1,
                                        "student": 1,
                                        "skip_conflicts": False
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def testRecurringBookingConflictFlagSet(self):
        Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=self.start_time,
            end_time=self.end_time
        ).save()

        request = self.factory.post("/recurring_booking",
                                    {
                                        "start_date": "2019-10-01",
                                        "end_date": "2019-10-16",
                                        "booking_start_time": "12:00",
                                        "booking_end_time": "15:00",
                                        "room": 1,
                                        "group": 1,
                                        "student": 1,
                                        "skip_conflicts": True
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCreate.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, [self.start_date])

    def testCancelRecurringBookingBeforeStart(self):
        recurring_booking, conflicts = RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.user1,
            False
        )

        with mock_datetime(datetime.datetime(2019, 9, 12, 11, 30, 0, 0), datetime):
            request = self.factory.post("/booking/{}/cancel_recurring_booking".format(recurring_booking.id),
                                        {}, format="json")
            force_authenticate(request, user=User.objects.get(username="john"))
            response = RecurringBookingCancel.as_view()(request, recurring_booking.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecurringBooking.objects.count(), 0)
        self.assertEqual(Booking.objects.count(), 0)

    def testCancelRecurringBookingAfterStart(self):
        recurring_booking, conflicts = RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.user1,
            False
        )
        self.assertEqual(recurring_booking.booking_set.count(), 3)

        with mock_datetime(datetime.datetime(2019, 10, 10, 11, 30, 0, 0), datetime):
            request = self.factory.post("/booking/{}/cancel_recurring_booking".format(recurring_booking.id),
                                        {}, format="json")
            force_authenticate(request, user=User.objects.get(username="john"))
            response = RecurringBookingCancel.as_view()(request, recurring_booking.id)

        recurring_booking = RecurringBooking.objects.get(id=recurring_booking.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RecurringBooking.objects.count(), 1)
        self.assertEqual(recurring_booking.booking_set.count(), 2)
        self.assertEqual(recurring_booking.end_date, datetime.date(2019, 10, 10))

    def testCancelRecurringBookingAfterEnd(self):
        recurring_booking, conflicts = RecurringBooking.objects.create_recurring_booking(
            self.start_date,
            self.end_date,
            self.start_time,
            self.end_time,
            self.room,
            self.group,
            self.user1,
            False
        )
        self.assertEqual(recurring_booking.booking_set.count(), 3)

        with mock_datetime(datetime.datetime(2019, 10, 17, 11, 30, 0, 0), datetime):
            request = self.factory.post("/booking/{}/cancel_recurring_booking".format(recurring_booking.id),
                                        {}, format="json")
            force_authenticate(request, user=User.objects.get(username="john"))
            response = RecurringBookingCancel.as_view()(request, recurring_booking.id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RecurringBooking.objects.count(), 1)
