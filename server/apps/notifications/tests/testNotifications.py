from django.test import TestCase
import datetime

from apps.accounts.models.User import User
from apps.booking.models.Booking import Booking
from apps.notifications.models.Notification import Notification
from apps.rooms.models.Room import Room


class TestNotification(TestCase):

    def setUp(self):
        self.user = User(username="user")
        self.user.save()

        self.room1 = Room(name="Room1", capacity=1, number_of_computers=1)
        self.room1.save()
        self.booker = User(username="username")
        self.booker.save()
        self.booking1 = Booking(
            room=self.room1,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(10, 0, 0),
            end_time=datetime.time(12, 0, 0),
            booker=self.booker
        )
        self.booking1.save()
        self.booking2 = Booking(
            room=self.room1,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(15, 0, 0),
            end_time=datetime.time(17, 0, 0),
            booker=self.booker
        )
        self.booking2.save()

        self.room2 = Room(name="Room2", capacity=1, number_of_computers=1)
        self.room2.save()
        self.booking3 = Booking(
            room=self.room2,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(10, 0, 0),
            end_time=datetime.time(12, 0, 0),
            booker=self.booker
        )
        self.booking3.save()
        self.booking4 = Booking(
            room=self.room2,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(16, 0, 0),
            end_time=datetime.time(17, 0, 0),
            booker=self.booker
        )
        self.booking4.save()

    def testNotificationRoomAvailabilitySuccess(self):
        notification = Notification(
            booker=self.user,
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(hours=3)
        )
        notification.save()
        notification.rooms.add(self.room1)
        result = notification.check_room_availability(self.room1)

        if not result:
            self.fail()

        self.assertEqual(result[0], datetime.time(12, 0, 0))
        self.assertEqual(result[1], datetime.time(15, 0, 0))

    def testNotificationRoomAvailabilitySuccessMultipleOptions(self):
        booking = Booking(
            room=self.room1,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(12, 30, 0),
            end_time=datetime.time(14, 0, 0),
            booker=self.booker
        )
        booking.save()
        notification = Notification(
            booker=self.user,
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(minutes=30)
        )
        notification.save()
        notification.rooms.add(self.room1)
        result = notification.check_room_availability(self.room1)

        if not result:
            self.fail()

        # Longest available range will be returned
        self.assertEqual(result[0], datetime.time(14, 0, 0))
        self.assertEqual(result[1], datetime.time(15, 0, 0))

    def testNotificationRoomAvailabilityFailure(self):
        notification = Notification(
            booker=self.user,
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(hours=8)
        )
        notification.save()
        notification.rooms.add(self.room1)
        result = notification.check_room_availability(self.room1)

        self.assertEqual(False, result)

    def testNotificationRoomAvailabilityMultipleRoomsSuccess(self):
        notification = Notification(
            booker=self.user,
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(hours=4)
        )
        notification.save()
        notification.rooms.add(self.room1, self.room2)
        result = notification.check_all_room_availability()

        if not result:
            self.fail()

        self.assertEqual(result[0], self.room2)
        self.assertEqual(result[1], datetime.time(12, 0, 0))
        self.assertEqual(result[2], datetime.time(16, 0, 0))

    def testNotificationRoomAvailabilityMultipleRoomsFailure(self):
        notification = Notification(
            booker=self.user,
            date=datetime.date(2020, 1, 1),
            range_start=datetime.time(11, 0, 0),
            range_end=datetime.time(16, 0, 0),
            minimum_booking_time=datetime.timedelta(hours=8)
        )
        notification.save()
        notification.rooms.add(self.room1, self.room2)
        result = notification.check_all_room_availability()

        self.assertEqual(False, result)
