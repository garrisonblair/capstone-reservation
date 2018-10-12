from django.test import TestCase
from unittest import mock

from ..WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter

class testWebCalendarExporter(TestCase):

    TEST_ICS = """BEGIN:VCALENDAR
METHOD:PUBLISH
BEGIN:VEVENT
UID:1
SUMMARY:Test Booking
DESCRIPTION:Test Bookings
CLASS:PUBLIC
STATUS:TENTATIVE
DTSTART:20181012T103000
DTEND:20181012T120000
END:VEVENT
END:VCALENDAR"""

    def setUp(self):
        self.exporter = WEBCalendarExporter()

    def testLoginSuccess(self):

        self.exporter.login()

    def testBackupBooking(self):

        serializerMock = mock.Mock()
        serializerMock.serialize_booking.return_value = self.TEST_ICS

        self.exporter = WEBCalendarExporter(ics_serializer=serializerMock)

        self.exporter.backup_booking(None)

