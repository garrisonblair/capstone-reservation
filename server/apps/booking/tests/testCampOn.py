from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.booking.models.CampOn import CampOn
from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from datetime import datetime
import re

class TestCampOn(TestCase):

    def setUp(self):
        #Setup one Student
        sid = '12345678'
        self.student = Student(student_id=sid)
        self.student.user = None
        self.student.save()
        
        #Setup one Room
        rid = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(room_id=rid, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        #Setup one Date and Time
        self.date = datetime.strptime("2019-09-29", "%Y-%m-%d").date()
        self.start_time = datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.strptime("13:00", "%H:%M").time()

        #Setup one Booking
        self.booking = Booking(student=self.student, room=self.room, date=self.date, start_time=self.start_time, end_time=self.end_time)
        self.booking.save()

    def testCampOnCreation(self):
        #Create a second Student for camp-on
        student_id = '87654321'
        campStudent = Student(student_id=student_id)
        campStudent.user = None
        campStudent.save()

        #Get the current time
        current_start_time = datetime.now().strftime('%H:%M')

        campon = CampOn(student=campStudent, booking=self.booking, start_time=current_start_time)
        campon.save()
        read_campon = CampOn.objects.get(student=campStudent, booking=self.booking, start_time=current_start_time)

        self.assertEqual(read_campon, campon)
        self.assertEqual(len(Booking.objects.all()), 1)
        print(str(read_campon))
        assert re.match(r'^Campon: \d+, Student: 87654321, Booking: 1, Start time: [0-9][0-9]:[0-9][0-9]:[0-9][0-9]$', str(read_campon))