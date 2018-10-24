from datetime import datetime
import json

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from ..models.Booking import Booking
from ..models.CampOn import CampOn

from ..views.campon import CampOnView

class CampOnAPITest(TestCase):
    def setUp(self):
        # Setup one Booking
        sid = '12345678'
        self.student = Student(student_id=sid)
        self.student.user = None
        self.student.save()

        rid = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(room_id=rid, 
                         capacity=capacity, 
                         number_of_computers=number_of_computers)
        self.room.save()

        self.date = datetime.strptime("2019-09-29", "%Y-%m-%d").date()
        self.start_time = datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.strptime("14:00", "%H:%M").time()

        self.booking = Booking(student=self.student,
                               room=self.room, 
                               date=self.date,
                               start_time=self.start_time,
                               end_time=self.end_time)
        self.booking.save()

         # Setup one user for CampOn
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        # Setup one student for the user
        student = Student(student_id="j_lenn")
        student.user = self.user
        student.save()

    def testCreateCampOnSuccess(self):
        request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "14:00"
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="john"))
        response = CampOnView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)