from django.test import TestCase
from apps.accounts.models.Booking import Booking
from apps.accounts.models.Student import Student
from apps.accounts.models.Room import Room
from datetime import datetime

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

        rid = "Room 1"
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
		