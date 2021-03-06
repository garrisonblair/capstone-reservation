import datetime

from unittest import mock

from django.apps import apps
from django.test.testcases import TestCase

from apps.booking.models.Booking import Booking
from apps.accounts.models.User import User
from apps.rooms.models.Room import Room


class TestExporterSetup(TestCase):

    def setUp(self):
        self.exporter_app_config = apps.get_app_config("booking_exporter")

        self.booker = User.objects.create_user(username="f_daigl",
                                               email="fred@email.com",
                                               password="password")
        self.booker.save()

        self.room = Room(name="Room 1")
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
