from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from datetime import datetime, time
import re
from django.core.exceptions import ValidationError

from apps.system_administration.models.system_settings import SystemSettings


class TestBooking(TestCase):
    def setUp(self):
        # Setup one booker
        sid = '12345678'
        self.booker = Booker(booker_id=sid)
        self.booker.user = None
        self.booker.save()

        # Setup one Room
        name = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        # Setup one Date and Time
        self.date = datetime.strptime("2019-09-29", "%Y-%m-%d").date()
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

    def activateMerging(self, threshold):
        settings = SystemSettings.get_settings()

        settings.merge_adjacent_bookings = True
        settings.merge_threshold_minutes = threshold

        settings.save()
