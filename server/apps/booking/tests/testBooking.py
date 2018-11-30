from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.booking.models.CampOn import CampOn
from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from datetime import datetime
import re
from django.core.exceptions import ValidationError


class TestBooking(TestCase):
    def setUp(self):
        # Setup one booker
        sid = '12345678'
        self.booker = Booker(booker_id=sid)
        self.booker.user = None
        self.booker.save()

        # Setup one booker2
        sid2 = '23456789'
        self.booker2 = Booker(booker_id=sid2)
        self.booker2.user = None
        self.booker2.save()

        # Setup one campon_booker
        sid3 = '87654321'
        self.campon_booker = Booker(booker_id=sid3)
        self.campon_booker.user = None
        self.campon_booker.save()

        # Setup one Room
        name = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        # Setup one Date and Time
        self.date = datetime.now().strftime("%Y-%m-%d")
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
        assert re.match(r'^Booking: \d+,'
                        r' Booker: 12345678,'
                        r' Room: 1,'
                        r' Date: 2019-09-29,'
                        r' Start time: 12:00:00,'
                        r' End Time: 13:00:00$', str(read_booking))

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

    def testOverlappedStartTimeCampOn(self):
        # Case with existing Booking from 12:00 to 13:00, then a CampOn is made on the Booking.
        # Afterward, the Booking is moved from 14 to 15:00 but 12:00 to 13:00 is still CampOned.
        booking = Booking(booker=self.booker,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        created_booking = Booking.objects.last()

        camp_on_start_time = datetime.strptime("12:15", "%H:%M").time()
        camp_on = CampOn.objects.create(booker=self.campon_booker,
                                        camped_on_booking=booking,
                                        start_time=camp_on_start_time,
                                        end_time=self.end_time)

        new_start_time = datetime.strptime("14:00", "%H:%M").time()
        new_end_time = datetime.strptime("15:00", "%H:%M").time()
        updated_booking = Booking.objects.filter(id=created_booking.id).update(start_time=new_start_time,
                                                                               end_time=new_end_time)

        start_time2 = datetime.strptime("12:00", "%H:%M").time()
        end_time2 = datetime.strptime("14:00", "%H:%M").time()
        booking2 = Booking(booker=self.booker2,
                           room=self.room,
                           date=self.date,
                           start_time=start_time2,
                           end_time=end_time2)
        with self.assertRaises(ValidationError) as ex:
            booking2.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testOverlappedEndTimeCampOn(self):
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

    def testOverlappedSameTimeCampOn(self):
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
