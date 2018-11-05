import datetime

from unittest import mock
from unittest.mock import Mock

from django.apps import apps
from django.test.testcases import TestCase

from apps.booking.models import Booking
from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room


class TestExporterSetup(TestCase):

    def setUp(self):
        self.exporter_app_config = apps.get_app_config("booking_exporter")

        self.booker = Booker(booker_id="f_daigl")
        self.booker.save()

        self.room = Room(room_id="Room 1")
        self.room.save()

    def testExporterNotifiedCreate(self):
        exporter_mock = mock.Mock()

        self.exporter_app_config.web_calendar_exporter = exporter_mock

        Booking.observers = [exporter_mock]

        booking = Booking(
            booker=self.booker,
            room=self.room,
            start_time=datetime.time(12, 0, 0),
            end_time=datetime.time(13, 0, 0),
            date=datetime.date(2018, 1, 1))
        booking.save()

        self.assertEqual(booking, exporter_mock.subject_created.call_args[0][0])
