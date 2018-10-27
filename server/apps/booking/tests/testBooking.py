from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from datetime import datetime
import re
from django.core.exceptions import ValidationError


class TestBooking(TestCase):

    def setUp(self):
        # Setup one Student
        sid = '12345678'
        self.student = Student(student_id=sid)
        self.student.user = None
        self.student.save()

        # Setup one Room
        rid = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(room_id=rid, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        # Setup one Date and Time
        self.date = datetime.strptime("2019-09-29", "%Y-%m-%d").date()
        self.start_time = datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.strptime("13:00", "%H:%M").time()

        # Get current size of the bookings
        self.lengthOfBookings = len(Booking.objects.all())

    def testBookingCreation(self):
        booking = Booking(student=self.student,
                          room=self.room, date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        read_booking = Booking.objects.get(student=self.student,
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
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking2 = Booking(student=self.student,
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
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking3 = Booking(student=self.student,
                           room=self.room,
                           date=self.date,
                           start_time=start_time3,
                           end_time=end_time3)

        with self.assertRaises(ValidationError) as ex:
            booking3.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testOverlappedSameTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 12:00 to 13:00
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking4 = Booking(student=self.student,
                           room=self.room,
                           date=self.date,
                           start_time=self.start_time,
                           end_time=self.end_time)

        with self.assertRaises(ValidationError) as ex:
            booking4.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 1)

    def testPassEndTimeSameAsStartTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 11:00 to 12:00. No error should be found
        start_time4 = datetime.strptime("11:00", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking5 = Booking(student=self.student,
                           room=self.room,
                           date=self.date,
                           start_time=start_time4,
                           end_time=self.start_time)

        booking5.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 2)

    def testPassStartTimeSameAsEndTimeBooking(self):
        # Case with existing time 12:00 to 13:00, compare to 11:00 to 12:00. No error should be found
        end_time4 = datetime.strptime("14:00", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=self.end_time)
        booking.save()
        booking5 = Booking(student=self.student,
                           room=self.room,
                           date=self.date,
                           start_time=self.end_time,
                           end_time=end_time4)
        booking5.save()
        self.assertEqual(len(Booking.objects.all()), self.lengthOfBookings + 2)

    def testFailWhenEndTimeBeforeStartTime(self):
        end_time = datetime.strptime("11:00", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=end_time)

        try:
            booking.save()
        except ValidationError:
            self.assertTrue(True)

    def testBookingStartTimeEarlierThanEarliestTime(self):
        booking_start_time = datetime.strptime("7:00", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=booking_start_time,
                          end_time=self.end_time)

        with self.assertRaises(ValidationError) as ex:
            booking.save()

    def testBookingStartTimeLaterThanLastTime(self):
        booking_start_time = datetime.strptime("23:05", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=booking_start_time,
                          end_time=self.end_time)

        with self.assertRaises(ValidationError) as ex:
            booking.save()

    def testBookingEndTimeEarlierThanEarliestTime(self):
        booking_end_time = datetime.strptime("7:00", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=booking_end_time)

        with self.assertRaises(ValidationError) as ex:
            booking.save()

    def testBookingEndTimeLaterThanLastTime(self):
        booking_end_time = datetime.strptime("23:05", "%H:%M").time()
        booking = Booking(student=self.student,
                          room=self.room,
                          date=self.date,
                          start_time=self.start_time,
                          end_time=booking_end_time)

        with self.assertRaises(ValidationError) as ex:
            booking.save()