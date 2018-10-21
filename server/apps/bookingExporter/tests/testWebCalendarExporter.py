import datetime

from django.test import TestCase
from unittest import mock

from ..WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter
from ..models.bookingExporterModels import ExternalRoomID

from apps.booking.models import Booking
from apps.rooms.models import Room
from apps.accounts.models import Student
from apps.calendar_administration.models import SystemSettings


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
        room = Room(room_id="Room 1")
        room.save()

        external_id = ExternalRoomID(external_id="_ROOM1_")
        external_id.room = room
        external_id.save()

        student = Student(student_id="s_loc")
        student.save()

        self.booking = Booking(start_time=datetime.time(12, 0, 0),
                               end_time=datetime.time(13, 0, 0),
                               date=datetime.date(2018, 10, 12),
                               student=student,
                               room=room)
        self.booking.save()

        self.response_mock = mock.Mock()
        self.response_mock.text = ""

        self.session_mock = mock.Mock()
        self.session_mock.post.return_value = self.response_mock

    def testLoginSuccess(self):

        settings = SystemSettings.get_settings()

        settings.webcalendar_username = "f_daigl"
        settings.webcalendar_password = "mySafePassword"
        settings.save()

        exporter = WEBCalendarExporter(self.session_mock)
        exporter.login()

        self.assertEqual(self.session_mock.post.call_count, 1)

        self.assertEqual(self.session_mock.post.call_args[1],
                         {"data": {
                                "login": settings.webcalendar_username,
                                "password": settings.webcalendar_password}
                          })

        self.assertEqual(self.session_mock.post.call_args[0][0],
                         WEBCalendarExporter.LOGIN_URL)

    def testBackupBooking(self):

        serializer_mock = mock.Mock()
        serializer_mock.serialize_booking.return_value = self.TEST_ICS

        self.exporter = WEBCalendarExporter(self.session_mock, serializer_mock)
        self.exporter.backup_booking(self.booking)

        self.assertEqual(serializer_mock.serialize_booking.call_args[0][0], self.booking)

        self.assertEqual(self.session_mock.post.call_args[0][0],
                         WEBCalendarExporter.IMPORT_HANDLER_URL)

        self.assertEqual(self.session_mock.post.call_args[1],
                         {'data': {
                            'overwrite': 'Y',
                            'calUser': self.booking.room.externalroomid.external_id,
                            'ImportType': 'ICAL',
                            'exc_private': '1'},
                         'files': {
                            'FileName': ('booking.ics', self.TEST_ICS)}
                          })
