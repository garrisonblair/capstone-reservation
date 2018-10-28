
import datetime

from django.test import TestCase
from unittest import mock

from apps.booking.models import Booking
from apps.rooms.models import Room
from apps.accounts.models import Student
from ..WEBCalendarExporter.ICSSerializer import ICSSerializer


class testWebCalendarExporter(TestCase):

    def setUp(self):

        room = Room(room_id="Room 19")
        room.save()

        student = Student(student_id="s_loc")
        student.save()

        self.booking = Booking(start_time=datetime.time(13, 0, 0),
                               end_time=datetime.time(14, 0, 0),
                               date=datetime.date(2018, 10, 28),
                               student=student,
                               room=room)

        self.booking.save()


    def testSerializeBooking(self):

        test = ICSSerializer()
        test.serialize_booking(self.booking)

        self.assertEquals(True, True)


