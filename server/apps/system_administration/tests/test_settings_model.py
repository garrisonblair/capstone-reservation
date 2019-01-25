from django.test import TestCase
from apps.system_administration.models.system_settings import SystemSettings
from apps.booking.models.Booking import Booking


class SettingsModelTests(TestCase):

    def setUp(self):

        self.system_settings = SystemSettings.get_settings()
        self.system_settings.save()

    def testActivateWebCalendarBackup(self):

        booking_observers_before_count = len(Booking.observers)

        self.system_settings.is_webcalendar_backup_active = True

        self.system_settings.save()

        booking_observers_after_count = len(Booking.observers)
        self.assertEqual(booking_observers_after_count, booking_observers_before_count + 1)

    def testDeactivateWebcalendarBackup(self):
        self.system_settings.is_webcalendar_backup_active = True
        self.system_settings.save()

        booking_observers_before_count = len(Booking.observers)

        self.system_settings.is_webcalendar_backup_active = False
        self.system_settings.save()

        booking_observers_after_count = len(Booking.observers)
        self.assertEqual(booking_observers_after_count, booking_observers_before_count - 1)
