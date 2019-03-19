import unittest

from django.test import TestCase
from datetime import date, time, datetime, timedelta

from apps.system_administration.models.system_settings import SystemSettings
from ..CamponCreateListener import CamponCreateListener

from apps.booking.models.CampOn import CampOn
from apps.booking.models.Booking import Booking
from apps.accounts.models.User import User
from apps.rooms.models.Room import Room


class TestCamponCreateListener(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("username1")
        self.user1.save()

        self.user2 = User.objects.create_user("username2")
        self.user2.save()

        self.room = Room(name="The Room")
        self.room.save()

        self.booking = Booking(date=date(2020, 1, 1),
                               start_time=time(12, 0, 0),
                               end_time=time(16, 0, 0),
                               booker=self.user1,
                               room=self.room)

        self.booking.save()

    @unittest.skip
    def testCamponsRefutableSet(self):

        settings = SystemSettings.get_settings()

        settings.campons_refutable = True
        settings.booking_time_to_expire_minutes = 10
        settings.save()

        campon = CampOn(booker=self.user2,
                        start_time=time(1, 0, 0),
                        end_time=time(2, 0, 0),
                        camped_on_booking=self.booking)

        now = datetime.now()

        campon_listener = CamponCreateListener()
        campon_listener.subject_created(campon)

        # But expiration into datetime to perform almostequal assertion
        exp_base = campon.camped_on_booking.expiration_base
        exp_base_datetime = datetime.today()
        exp_base_datetime.replace(hour=exp_base.hour,
                                  minute=exp_base.minute,
                                  second=exp_base.second,
                                  microsecond=exp_base.microsecond)

        self.assertAlmostEqual(now, exp_base_datetime, delta=timedelta(seconds=1))
        self.assertFalse(campon.camped_on_booking.confirmed)
