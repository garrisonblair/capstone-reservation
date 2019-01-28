from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from datetime import datetime, time, timedelta

from django.core.exceptions import ValidationError
from django.core.management import call_command

from apps.system_administration.models.system_settings import SystemSettings
from apps.accounts.models.User import User
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.exceptions import PrivilegeError


class TestBooking(TestCase):
    def setUp(self):
        # Setup one booker
        self.booker = User.objects.create_user(username="f_daigl",
                                               email="fred@email.com",
                                               password="safe_password")  # type: User
        self.booker.save()

        # Setup one Room
        name = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        # Setup one Date and Time
        self.date = datetime.now().date()
        self.start_time = datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.strptime("13:00", "%H:%M").time()

        # Get current size of the bookings
        self.lengthOfBookings = len(Booking.objects.all())

    def testBookingCreation(self):
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        read_booking = Booking.objects.get(booker=self.booker,
                                           room=self.room,
                                           date=self.date,
                                           start_time=self.start_time,
                                           end_time=self.end_time)

        self.assertEqual(read_booking, booking)
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testOverlappedStartTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 12:30 to 13:00
        start_time2 = datetime.strptime("12:30", "%H:%M").time()
        end_time2 = datetime.strptime("13:00", "%H:%M").time()

        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=start_time2,
                           end_time=end_time2)

        with self.assertRaises(ValidationError) as ex:
            booking2.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testOverlappedEndTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 11:30 to 12:30
        start_time3 = datetime.strptime("11:30", "%H:%M").time()
        end_time3 = datetime.strptime("12:30", "%H:%M").time()

        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking3 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=start_time3,
                           end_time=end_time3)

        with self.assertRaises(ValidationError) as ex:
            booking3.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testOverlappedSameTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 12:00 to 13:00
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking4 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=self.start_time,
                           end_time=self.end_time)

        with self.assertRaises(ValidationError) as ex:
            booking4.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testPassEndTimeSameAsStartTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 11:00 to 12:00. No errors should be found
        start_time4 = datetime.strptime("11:00", "%H:%M").time()
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking5 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=start_time4,
                           end_time=self.start_time)

        booking5.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 2)

    def testPassStartTimeSameAsEndTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 11:00 to 12:00. No errors should be found
        end_time4 = datetime.strptime("14:00", "%H:%M").time()
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking5 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=self.end_time,
                           end_time=end_time4)
        booking5.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 2)

    def testFailWhenEndTimeBeforeStartTime(self):
        end_time = datetime.strptime("11:00", "%H:%M").time()
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=end_time)

        try:
            booking.save()
        except ValidationError:
            self.assertTrue(True)
            return
        self.fail()

    def testMergeBookingExactMatchStart(self):
        self.activateMerging(0)

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(12, 0),
                           end_time=time(13, 0))

        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(11, 0),
                           end_time=time(12, 0))

        booking2.save()
        booking2.merge_with_neighbouring_bookings()

        self.assertEqual(booking2.end_time, booking1.end_time)

        try:
            booking1.refresh_from_db()
        except Booking.DoesNotExist:
            self.assertTrue(True)
            return

        self.fail("Merged booking not deleted")

    def testMergeBookingExactMatchEnd(self):
        self.activateMerging(0)

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(12, 0),
                           end_time=time(13, 0))

        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(13, 0),
                           end_time=time(14, 0))

        booking2.save()
        booking2.merge_with_neighbouring_bookings()

        self.assertEqual(booking2.start_time, booking1.start_time)

        try:
            booking1.refresh_from_db()
        except Booking.DoesNotExist:
            self.assertTrue(True)
            return

        self.fail("Merged booking not deleted")

    def testMergeBookingStartInThreshold(self):
        self.activateMerging(15)

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(12, 0),
                           end_time=time(13, 0))

        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(13, 10),
                           end_time=time(14, 0))

        booking2.save()
        booking2.merge_with_neighbouring_bookings()

        self.assertEqual(booking2.start_time, booking1.start_time)

        try:
            booking1.refresh_from_db()
        except Booking.DoesNotExist:
            self.assertTrue(True)
            return

        self.fail("Merged booking not deleted")

    def testMergeBookingEndInThreshold(self):
        self.activateMerging(15)

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(12, 0),
                           end_time=time(13, 0))

        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(10, 0),
                           end_time=time(11, 50))

        booking2.save()
        booking2.merge_with_neighbouring_bookings()

        self.assertEqual(booking2.end_time, booking1.end_time)

        try:
            booking1.refresh_from_db()
        except Booking.DoesNotExist:
            self.assertTrue(True)
            return

        self.fail("Merged booking not deleted")

    def testMergeBookingStartAndEnd(self):
        self.activateMerging(0)

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(12, 0),
                           end_time=time(13, 0))

        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(14, 0),
                           end_time=time(15, 0))

        booking2.save()

        booking3 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(13, 0),
                           end_time=time(15, 0))

        booking3.merge_with_neighbouring_bookings()

        self.assertEqual(booking3.end_time, booking2.end_time)
        self.assertEqual(booking3.start_time, booking1.start_time)

        try:
            booking1.refresh_from_db()
            booking2.refresh_from_db()
        except Booking.DoesNotExist:
            self.assertTrue(True)
            return

        self.fail("Merged booking not deleted")

    def testBypassPrivilegeBooking(self):
        call_command("loaddata", "apps/accounts/fixtures/privilege_categories.json")

        privilege = PrivilegeCategory.objects.get(is_default=True)  # type: PrivilegeCategory

        privilege.max_num_bookings_for_date = 1
        privilege.save()

        self.booker.bookerprofile.privilege_categories.add(privilege)
        self.booker.save()

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(12, 0),
                           end_time=time(15, 0))

        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date,
                           start_time=time(16, 0),
                           end_time=time(18, 0))
        try:
            booking2.save()
        except PrivilegeError:
            privilege_error = True

        if not privilege_error:
            self.fail("Privilege not evaluated")

        booking2.bypass_privileges = True

        try:
            booking2.save()
        except PrivilegeCategory:
            self.fail("Privilege should not be evaluated")
            return

        self.assertTrue(True)

    def activateMerging(self, threshold):
        settings = SystemSettings.get_settings()

        settings.merge_adjacent_bookings = True
        settings.merge_threshold_minutes = threshold

        settings.save()

    def testGetBookingDuration(self):
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=time(13, 0),
                          end_time=time(15, 0))

        self.assertEqual(booking.get_duration(), timedelta(hours=2))
