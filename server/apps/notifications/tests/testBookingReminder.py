import datetime
from unittest.mock import Mock
from unittest import mock
from unittest import skip


from django.test import TestCase

from apps.notifications.models.BookingReminder import BookingReminder

from apps.booking.models.Booking import Booking
from apps.accounts.models.User import User
from apps.rooms.models.Room import Room

from apps.util.mock_datetime import mock_datetime

from apps.system_administration.models.system_settings import SystemSettings


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
        reminder.send()

        self.assertEqual(self.user.send_email.call_count, 1)

    @skip
    def testBookingReminderManagerSendReminders(self):
        settings = SystemSettings.get_settings()
        settings.default_time_to_notify_before_booking = datetime.timedelta(hours=1)
        settings.save()

        reminder1 = BookingReminder.objects.create_reminder(self.booking, datetime.timedelta(hours=1))
        reminder2 = BookingReminder.objects.create_reminder(self.booking, datetime.timedelta(hours=1, minutes=1))
        reminder3 = BookingReminder.objects.create_reminder(self.booking, datetime.timedelta(minutes=5))

        reminder1.save()
        reminder2.save()
        reminder3.save()

        with mock_datetime(datetime.datetime(2019, 3, 10, 11, 2, 0), datetime):
            BookingReminder.objects.send_reminders()

        with self.assertRaises(BookingReminder.DoesNotExist):
            reminder1.refresh_from_db()

        with self.assertRaises(BookingReminder.DoesNotExist):
            reminder2.refresh_from_db()

        reminder3.refresh_from_db()
