
import datetime

from django.test import TestCase

from apps.booking.models import Booking
from apps.rooms.models import Room
from apps.accounts.models.User import User
from ..WEBCalendarExporter.ICSSerializer import ICSSerializer
from apps.groups.models import Group


class testWebCalendarExporter(TestCase):

    def setUp(self):

        room = Room(name="Room 19")
        room.save()

        booker = User.objects.create_user(username="s_loc")
        booker.save()

        booker2 = User.objects.create_user(username="f_daigl")
        booker2.save()

        self.booking = Booking(start_time=datetime.time(13, 0, 0),
                               end_time=datetime.time(14, 0, 0),
                               date=datetime.date(2018, 10, 28),
                               booker=booker,
                               room=room)

        self.booking.save()

        group = Group(name='Test Group',
                      is_verified=True,
                      owner=booker)

        group.save()

        group.members.add(booker)
        group.members.add(booker2)

        self.booking2 = Booking(start_time=datetime.time(14, 0, 0),
                                end_time=datetime.time(15, 0, 0),
                                date=datetime.date(2018, 10, 28),
                                booker=booker,
                                group=group,
                                room=room)

        self.booking2.save()

    def returnSerializedICSPredefinedNoGroup(self):

        ics_file = """BEGIN:VCALENDAR
METHOD:PUBLISH
BEGIN:VEVENT
UID: 1
SUMMARY:Booker: s_loc, Group: None
DESCRIPTION:Booker: s_loc, Group: None
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
SUMMARY:Booker: s_loc, Group: Test Group
DESCRIPTION:Booker: s_loc, Group: Test Group
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
