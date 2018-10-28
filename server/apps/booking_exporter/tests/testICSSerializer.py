
import datetime

from django.test import TestCase
from unittest import mock

from apps.booking.models import Booking
from apps.rooms.models import Room
from apps.accounts.models import Student
from ..WEBCalendarExporter.ICSSerializer import ICSSerializer
from apps.groups.models import StudentGroup


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

        group = StudentGroup(name='Test Group',
                             students=self.student,
                             is_verified=True)

        self.booking2 = Booking(start_time=datetime.time(13, 0, 0),
                                end_time=datetime.time(14, 0, 0),
                                date=datetime.date(2018, 10, 28),
                                student=student,
                                student_group=group,
                                room=room)

        self.booking2.save()


    def returnSerializedICSPredefinedNoGroup(self):

        ics_file = """BEGIN:VCALENDAR
METHOD:PUBLISH
BEGIN:VEVENT
UID: 1
SUMMARY:Student: s_loc, Group: None
DESCRIPTION:Student: s_loc, Group: None
CLASS:PUBLIC
STATUS:TENTATIVE
DTSTART:DTSTART:20181028T130000
DTEND:DTEND:20181028T140000
END:VEVENT
END:VCALENDAR"""

        return ics_file

    def returnSerializedICSPredefinedWithGroup(self):
        ics_file = """BEGIN:VCALENDAR
METHOD:PUBLISH
BEGIN:VEVENT
UID: 1
SUMMARY:Student: s_loc, Group: Test Group
DESCRIPTION:Student: s_loc, Group: Test Group
CLASS:PUBLIC
STATUS:TENTATIVE
DTSTART:DTSTART:20181028T130000
DTEND:DTEND:20181028T140000
END:VEVENT
END:VCALENDAR"""

        return ics_file


    def testICSSerializeBooking(self):

        test = ICSSerializer()

        generated = test.serialize_booking(self.booking)
        predefinedNoGroup = str(self.returnSerializedICSPredefinedNoGroup())

        self.assertEquals(generated, predefinedNoGroup)



    def testICSSerializeBookingWithGroup(self):

        test = ICSSerializer()

        generated = test.serialize_booking(self.booking2)
        predefinedWithGroup = str(self.returnSerializedICSPredefinedWithGroup())

        self.assertEquals(generated, predefinedWithGroup)


