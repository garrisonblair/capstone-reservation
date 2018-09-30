from django.test import TestCase
from apps.accounts.models.Booking import Booking
from apps.accounts.models.Student import Student
from apps.accounts.models.Room import Room
from datetime import datetime
import re

class TestBooking(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBookingCreation(self):
        sid = '12345678'

        student = Student(student_id=sid)
        student.user = None
        student.save()

        rid = "1"
        capacity = 7
        number_of_computers = 2

        room = Room(room_id=rid, capacity=capacity, number_of_computers=number_of_computers)
        room.save()
		
        date = datetime.strptime("2019-09-29", "%Y-%m-%d").date()
        start_time = datetime.strptime("12:00", "%H:%M").time()
        end_time = datetime.strptime("13:00", "%H:%M").time()

        booking = Booking(student=student, room=room, date=date, start_time=start_time, end_time=end_time)
        booking.save()

        read_booking = Booking.objects.get(student=student, room=room, date=date, start_time=start_time, end_time=end_time)
		
        self.assertEqual(read_booking, booking)		
        assert re.match(r'^Booking: \d+, Student: 12345678, Room: 1, Date: 2019-09-29, Start time: 12:00:00, End Time: 13:00:00$', str(read_booking))
		
    def testOverlappedBookingCreation(self):
        sid1 = '12345678'

        student1 = Student(student_id=sid1)
        student1.user = None
        student1.save()
		
        sid2 = '22222222'

        student2 = Student(student_id=sid2)
        student2.user = None
        student2.save()

        rid = "1"
        capacity = 7
        number_of_computers = 2

        room = Room(room_id=rid, capacity=capacity, number_of_computers=number_of_computers)
        room.save()
		
        date = datetime.strptime("2019-09-29", "%Y-%m-%d").date()
		
        start_time1 = datetime.strptime("12:00", "%H:%M").time()
        end_time1 = datetime.strptime("13:00", "%H:%M").time()
		
        start_time2 = datetime.strptime("12:30", "%H:%M").time()
        end_time2 = datetime.strptime("13:00", "%H:%M").time()

        booking = Booking(student=student1, room=room, date=date, start_time=start_time1, end_time=end_time1)
        booking.save()
		
        booking2 = Booking(student=student2, room=room, date=date, start_time=start_time2, end_time=end_time2)
        booking2.save()
		
        self.assertEqual(len(Booking.objects.all()), 1)
		
        start_time3 = datetime.strptime("1:30", "%H:%M").time()
        end_time3 = datetime.strptime("12:00", "%H:%M").time()
		
        booking3 = Booking(student=student2, room=room, date=date, start_time=start_time3, end_time=end_time3)
        booking3.save()
		
        self.assertEqual(len(Booking.objects.all()), 1)
		
        booking4 = Booking(student=student1, room=room, date=date, start_time=start_time1, end_time=end_time1)
        booking4.save()
		
        self.assertEqual(len(Booking.objects.all()), 1)
        self.assertEqual(len(Booking.objects.filter(student=student1, room=room, date=date, start_time=start_time1, end_time=end_time1)), 1)
        self.assertEqual(len(Booking.objects.filter(student=student2, room=room, date=date, start_time=start_time1, end_time=end_time1)), 0)
		