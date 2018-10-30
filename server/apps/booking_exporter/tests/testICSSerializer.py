
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
        student2 = Student(student_id="f_daigl")

        student.save()

        self.booking = Booking(start_time=datetime.time(13, 0, 0),
                               end_time=datetime.time(14, 0, 0),
                               date=datetime.date(2018, 10, 28),
                               student=student,
                               room=room)

        self.booking.save()

        group = StudentGroup(name='Test Group',
                             is_verified=True)

        group.save()

        group.students.set(student.student_id)
        group.students.set(student2.student_id)

        self.booking2 = Booking(start_time=datetime.time(14, 0, 0),
                                end_time=datetime.time(15, 0, 0),
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
UID: 2
SUMMARY:Student: s_loc, Group: Test Group
DESCRIPTION:Student: s_loc, Group: Test Group
CLASS:PUBLIC
STATUS:TENTATIVE
DTSTART:DTSTART:20181028T140000
DTEND:DTEND:20181028T150000
END:VEVENT
END:VCALENDAR"""

        return ics_file

    def testICSSerializeBookingNoGroup(self):

        test = ICSSerializer()

        generated = test.serialize_booking(self.booking)
        predefined_no_group = str(self.returnSerializedICSPredefinedNoGroup())

        self.assertEquals(generated, predefined_no_group)

    def testICSSerializeBookingWithGroup(self):

        test = ICSSerializer()

        generated = test.serialize_booking(self.booking2)
        predefined_with_group = str(self.returnSerializedICSPredefinedWithGroup())

        self.assertEquals(generated, predefined_with_group)
