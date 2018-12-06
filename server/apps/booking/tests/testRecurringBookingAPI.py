import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ContentType, ADDITION, CHANGE
from datetime import timedelta, datetime

from apps.accounts.models.Booker import Booker
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.Booking import Booking
from apps.groups.models import Group
from apps.rooms.models.Room import Room

from ..views.recurring_booking import RecurringBookingCreate

from ..serializers.recurring_booking import RecurringBookingSerializer
from ..serializers.booking import BookingSerializer


class BookingAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        booker1 = Booker(booker_id="j_lenn")
        booker1.user = self.user
        booker1.save()

        sid = '00000002'
        booker2 = Booker(booker_id=sid)
        booker2.user = None
        booker2.save()

        # Create student group
        name = "Students group"
        self.group = Group(name=name, is_verified=True, owner=booker1)
        self.group.save()
        self.group.members.add(booker1)
        self.group.members.add(booker2)

        self.room = Room(name="H833-17", capacity=4, number_of_computers=1)
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
        self.assertEqual(booking1.booker, self.group.members.get(booker_id='j_lenn'))

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.group, self.group)
        self.assertEqual(booking2.booker, self.group.members.get(booker_id='j_lenn'))

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

        self.assertEqual(booking3.start_time, self.start_time)
        self.assertEqual(booking3.end_time, self.end_time)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.group, self.group)
        self.assertEqual(booking3.booker, self.group.members.get(booker_id='j_lenn'))

        # LogEntry test
        all_recurring_booking_logs = LogEntry.objects.all()
        latest_recurring_booking_log = all_recurring_booking_logs.order_by('action_time')[0]
        self.assertEqual(latest_recurring_booking_log.action_flag, ADDITION)
        self.assertEqual(latest_recurring_booking_log.object_id, str(recurring_booking.id))
        self.assertEqual(latest_recurring_booking_log.user, self.user)
        self.assertEqual(latest_recurring_booking_log.object_repr,
                         json.dumps(RecurringBookingSerializer(recurring_booking).data))

        for booking in recurring_booking.booking_set.all():
            booking_logs = LogEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(booking),
                object_id=str(booking.id))
            latest_booking_log = booking_logs.order_by('action_time')[0]

            self.assertEqual(latest_booking_log.action_flag, ADDITION)
            self.assertEqual(latest_booking_log.object_id, str(booking.id))
            self.assertEqual(latest_booking_log.user, self.user)
            self.assertEqual(latest_booking_log.object_repr,
                             json.dumps(BookingSerializer(booking).data))

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
            booker=self.group.members.get(booker_id='j_lenn'),
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
            booker=self.group.members.get(booker_id='j_lenn'),
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
