from django.test import TestCase
import datetime

from apps.accounts.models.User import User
from apps.booking.models.Booking import Booking
from apps.notifications.models.Notification import Notification
from apps.rooms.models.Room import Room


class TestNotification(TestCase):

    def setUp(self):
        self.room = Room(name="Name", capacity=1, number_of_computers=1)
        self.room.save()
        self.booker = User(username="username")
        self.booker.save()
        self.booking1 = Booking(
            room=self.room,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(10, 0, 0),
            end_time=datetime.time(12, 0, 0),
            booker=self.booker
        )
        self.booking1.save()
        self.booking2 = Booking(
            room=self.room,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(15, 0, 0),
            end_time=datetime.time(17, 0, 0),
            booker=self.booker
        )
        self.booking2.save()

    def testNotificationRoomAvailabilitySuccess(self):
        notification = Notification(
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(hours=3)
        )
        notification.save()
        notification.rooms.add(self.room)
        result = notification.check_room_availability(self.room)

        if not result:
            self.fail()

        self.assertEqual(result[0], datetime.time(12, 0, 0))
        self.assertEqual(result[1], datetime.time(15, 0, 0))

    def testNotificationRoomAvailabilitySuccessMultipleOptions(self):
        booking = Booking(
            room=self.room,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(12, 30, 0),
            end_time=datetime.time(14, 0, 0),
            booker=self.booker
        )
        booking.save()
        notification = Notification(
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(minutes=30)
        )
        notification.save()
        notification.rooms.add(self.room)
        start, end = notification.check_room_availability(self.room)

        # Longest available range will be returned
        self.assertEqual(start, datetime.time(14, 0, 0))
        self.assertEqual(end, datetime.time(15, 0, 0))

    def testNotificationRoomAvailabilityFailure(self):
        notification = Notification(
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(hours=8)
        )
        notification.save()
        notification.rooms.add(self.room)
        result = notification.check_room_availability(self.room)

        self.assertEqual(False, result)
