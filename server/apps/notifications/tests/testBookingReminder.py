import datetime
from unittest.mock import Mock


from django.test import TestCase

from apps.notifications.models.BookingReminder import BookingReminder

from apps.booking.models.Booking import Booking
from apps.accounts.models.User import User
from apps.rooms.models.Room import Room


class TestBookingReminder(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user_1")
        self.user.save()

        self.room = Room(name="Room 1")
        self.room.save()

        self.booking = Booking.objects.create_booking(self.user,
                                                      None,
                                                      self.room,
                                                      datetime.date(2019, 3, 10),
                                                      datetime.time(12, 0, 0),
                                                      datetime.time(13, 0, 0))

        self.booking.save()

    def testCreateBookingReminderOneDay(self):

        reminder = BookingReminder.objects.create_reminder(self.booking, datetime.timedelta(days=1))

        self.assertEqual(reminder.booking, self.booking)
        self.assertEqual(reminder.reminder_time, datetime.datetime(2019, 3, 9, 12, 0, 0))

    def testCreateBookingReminder2Hours(self):

        reminder = BookingReminder.objects.create_reminder(self.booking, datetime.timedelta(hours=2))

        self.assertEqual(reminder.booking, self.booking)
        self.assertEqual(reminder.reminder_time, datetime.datetime(2019, 3, 10, 10, 0, 0))

    def testBookingReminderRemind(self):
        self.user.send_email = Mock()

        reminder = BookingReminder.objects.create_reminder(self.booking, datetime.timedelta(days=1))
        reminder.remind()

        self.assertEqual(self.user.send_email.call_count, 1)
