import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ContentType, ADDITION, CHANGE
from datetime import timedelta, datetime

from apps.accounts.models.User import User
from apps.booking.models.RecurringBooking import RecurringBooking
from apps.booking.models.Booking import Booking
from apps.groups.models.Group import Group
from apps.rooms.models.Room import Room

from apps.booking.views.recurring_booking import RecurringBookingCreate, RecurringBookingCancel, RecurringBookingEdit

from apps.booking.serializers.recurring_booking import RecurringBookingSerializer
from apps.booking.serializers.booking import BookingSerializer
from apps.rooms.serializers.room import RoomSerializer
from apps.booking.serializers.recurring_booking import LogRecurringBookingSerializer
from apps.booking.serializers.booking import LogBookingSerializer


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
        self.assertEqual(booking1.booker, self.user1)

        booking2 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=7))

        self.assertEqual(booking2.start_time, self.start_time)
        self.assertEqual(booking2.end_time, self.end_time)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.group, self.group)
        self.assertEqual(booking2.booker, self.user1)

        booking3 = recurring_booking.booking_set.get(date=self.start_date + timedelta(days=14))

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

    def testCancelRecurringBookingAllInstancesSuccess(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(earliest_booking.id) + "/cancel_recurring_booking",
                                    {
                                        "delete_all_instances": True
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCancel.as_view()(request, earliest_booking.id)
        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bookings.count(), 0)

    def testCancelRecurringBookingAllInstancesFailureNonExistentBooking(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(999) + "/cancel_recurring_booking",
                                    {
                                        "delete_all_instances": True
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCancel.as_view()(request, 999)
        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        self.assertRaises(Booking.DoesNotExist)
        self.assertEqual(bookings.count(), 3)

    def testCancelRecurringBookingSingleInstanceFailureNonExistentBooking(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(999) + "/cancel_recurring_booking",
                                    {
                                        "delete_all_instances": False,
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCancel.as_view()(request, 999)
        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        self.assertRaises(Booking.DoesNotExist)
        self.assertEqual(bookings.count(), 3)

    def testEditRecurringBookingAllInstancesSuccess(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        earliest_booking = bookings[0]

        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room.id, self.room.id)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room.id, self.room.id)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room.id, self.room.id)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        request = self.factory.post("booking/" + str(earliest_booking.id) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": True,
                                        "room": edited_room.id,
                                        "booking_start_time": str(edited_start_time)[:5],
                                        "booking_end_time": str(edited_end_time)[:5]
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingEdit.as_view()(request, earliest_booking.id)
        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        self.assertEqual(bookings.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(booking1.start_time, edited_start_time)
        self.assertEqual(booking1.end_time, edited_end_time)
        self.assertEqual(booking1.room.id, edited_room.id)

        self.assertEqual(booking2.start_time, edited_start_time)
        self.assertEqual(booking2.end_time, edited_end_time)
        self.assertEqual(booking2.room.id, edited_room.id)

        self.assertEqual(booking3.start_time, edited_start_time)
        self.assertEqual(booking3.end_time, edited_end_time)
        self.assertEqual(booking3.room.id, edited_room.id)

    def testEditRecurringBookingAllInstancesFailureMultiDateChange(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        earliest_booking = bookings[0]

        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room.id, self.room.id)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room.id, self.room.id)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room.id, self.room.id)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        request = self.factory.post("booking/" + str(earliest_booking.id) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": True,
                                        "room": edited_room.id,
                                        "date": edited_date,
                                        "booking_start_time": str(edited_start_time)[:5],
                                        "booking_end_time": str(edited_end_time)[:5]
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingEdit.as_view()(request, earliest_booking.id)
        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        self.assertEqual(bookings.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

    def testEditRecurringBookingAllInstancesFailureInvalidNonExistentBooking(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        earliest_booking = bookings[0]

        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room.id, self.room.id)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room.id, self.room.id)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room.id, self.room.id)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        request = self.factory.post("booking/" + str(999) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": True,
                                        "room": edited_room.id,
                                        "date": edited_date,
                                        "booking_start_time": str(edited_start_time)[:5],
                                        "booking_end_time": str(edited_end_time)[:5]
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingEdit.as_view()(request, 999)
        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)

        self.assertEqual(bookings.count(), 3)
        self.assertRaises(Booking.DoesNotExist)

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

    def testEditRecurringBookingSingleInstanceFailureNonExistentBooking(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-02 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-02 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(999) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": False,
                                        "room": edited_room.id,
                                        "booking_start_time": str(edited_start_time)[:5],
                                        "booking_end_time": str(edited_end_time)[:5],
                                        "date": edited_date,
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingEdit.as_view()(request, 999)

        self.assertRaises(Booking.DoesNotExist)

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        booking1 = Booking.objects.get(id=earliest_booking.id)

        self.assertEqual(bookings.count(), 3)

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

    def testCancelRecurringBookingMultiInstanceFailureNonExistentBooking(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-02 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-02 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(999) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": True,
                                        "room": edited_room.id,
                                        "booking_start_time": str(edited_start_time)[:5],
                                        "booking_end_time": str(edited_end_time)[:5],
                                        "date": edited_date,
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RecurringBookingCancel.as_view()(request, 999)

        self.assertRaises(Booking.DoesNotExist)

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        booking1 = Booking.objects.get(id=earliest_booking.id)

        self.assertEqual(bookings.count(), 3)

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

    def testEditRecurringBookingFailureNotOwner(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-02 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-02 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(earliest_booking.id) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": False,
                                        "room": edited_room.id,
                                        "booking_start_time": str(edited_start_time)[:5],
                                        "booking_end_time": str(edited_end_time)[:5],
                                        "date": edited_date,
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="f_daigl"))

        response = RecurringBookingEdit.as_view()(request, earliest_booking.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        booking1 = Booking.objects.get(id=earliest_booking.id)

        self.assertEqual(bookings.count(), 3)

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

    def testDeleteRecurringBookingFailureNotOwner(self):

        start1 = datetime.strptime("2019-10-01 12:00", "%Y-%m-%d %H:%M")
        end1 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date1 = start1.date()
        end_date1 = end1.date()
        start_time1 = start1.time()
        end_time1 = end1.time()

        start2 = datetime.strptime("2019-10-08 12:00", "%Y-%m-%d %H:%M")
        end2 = datetime.strptime("2019-10-08 15:00", "%Y-%m-%d %H:%M")
        start_date2 = start2.date()
        end_date2 = end2.date()
        start_time2 = start2.time()
        end_time2 = end2.time()

        start3 = datetime.strptime("2019-10-15 12:00", "%Y-%m-%d %H:%M")
        end3 = datetime.strptime("2019-10-15 15:00", "%Y-%m-%d %H:%M")
        start_date3 = start3.date()
        end_date3 = end3.date()
        start_time3 = start3.time()
        end_time3 = end3.time()

        recurring_booking = RecurringBooking(
            start_date=start_date1,
            end_date=end_date1,
            booking_start_time=start_time1,
            booking_end_time=end_time1,
            room=self.room,
            group=None,
            booker=self.user1,
            skip_conflicts=True
        ).save()

        recurring_booking = RecurringBooking.objects.get(start_date=start_date1,
                                                         end_date=end_date1,
                                                         booking_start_time=start_time1,
                                                         booking_end_time=end_time1,
                                                         room=self.room,
                                                         group=None,
                                                         booker=self.user1,
                                                         skip_conflicts=True)

        booking1 = Booking(
            booker=self.user1,
            room=self.room,
            date=self.start_date,
            start_time=start_time1,
            end_time=end_time1,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking2 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date2,
            start_time=start_time2,
            end_time=end_time2,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        booking3 = Booking(
            booker=self.user1,
            room=self.room,
            date=start_date3,
            start_time=start_time3,
            end_time=end_time3,
            recurring_booking=recurring_booking,
            confirmed=False
        ).save()

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        self.assertEqual(bookings.count(), 3)

        booking1 = bookings[0]
        booking2 = bookings[1]
        booking3 = bookings[2]

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)

        edited_start = datetime.strptime("2019-10-02 12:00", "%Y-%m-%d %H:%M")
        edited_end = datetime.strptime("2019-10-02 15:00", "%Y-%m-%d %H:%M")
        edited_date = edited_start.date()
        edited_start_time = edited_start.time()
        edited_end_time = edited_end.time()

        edited_room = Room.objects.get(name="H833-17")

        earliest_booking = bookings[0]
        for booking in bookings:
            if booking.id < earliest_booking.id:
                earliest_booking = booking

        request = self.factory.post("booking/" + str(earliest_booking.id) + "/edit_recurring_booking",
                                    {
                                        "edit_all_instances": False,
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="f_daigl"))

        response = RecurringBookingCancel.as_view()(request, earliest_booking.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        bookings = Booking.objects.all().filter(recurring_booking=recurring_booking)
        booking1 = Booking.objects.get(id=earliest_booking.id)

        self.assertEqual(bookings.count(), 3)

        self.assertEqual(booking1.start_time, start_time1)
        self.assertEqual(booking1.end_time, end_time1)
        self.assertEqual(booking1.room, self.room)
        self.assertEqual(booking1.date, start_date1)

        self.assertEqual(booking2.start_time, start_time2)
        self.assertEqual(booking2.end_time, end_time2)
        self.assertEqual(booking2.room, self.room)
        self.assertEqual(booking2.date, start_date2)

        self.assertEqual(booking3.start_time, start_time3)
        self.assertEqual(booking3.end_time, end_time3)
        self.assertEqual(booking3.room, self.room)
        self.assertEqual(booking3.date, start_date3)
