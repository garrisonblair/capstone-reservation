import datetime
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

        rid = "H800-1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(room_id=rid, 
                         capacity=capacity, 
                         number_of_computers=number_of_computers)
        self.room.save()

        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.start_time = datetime.datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.datetime.strptime("14:00", "%H:%M").time()

        self.booking = Booking(student=self.student,
                               room=self.room, 
                               date=self.date,
                               start_time=self.start_time,
                               end_time=self.end_time)
        self.booking.save()

         # Setup one user for CampOn
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='solji',
                                             email='solji@exid.com',
                                             password='kingmask')
        self.user.save()

        # Setup one student for the user
        self.student = Student(student_id="sol_ji")
        self.student.user = self.user
        self.student.save()

# CampOn start time by default is the current time. However, the current time cannot be used in the test, otherwise, the test will fail if it runs at midnight
# So the start time in this test will be assigned values

    def testCreateCampOnSuccess(self):
        request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "14:00"
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="solji"))
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_campon = CampOn.objects.last()
        self.assertEqual(created_campon.student, Student.objects.get(student_id='sol_ji'))
        self.assertEqual(created_campon.booking, Booking.objects.get(id=1))
        self.assertEqual(created_campon.start_time, datetime.time(12, 20))
        self.assertEqual(created_campon.end_time, datetime.time(14, 00))

    def testCreateCampOnWithBooking(self):
        request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "15:00"
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="solji"))
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_campon = CampOn.objects.last()
        self.assertEqual(created_campon.student, Student.objects.get(student_id='sol_ji'))
        self.assertEqual(created_campon.booking, Booking.objects.get(id=1))
        self.assertEqual(created_campon.start_time, datetime.time(12, 20))
        self.assertEqual(created_campon.end_time, datetime.time(14, 00))

        # Verify number of Booking
        self.assertEqual(len(Booking.objects.all()), 2)

        # Verify the content of the created Booking
        created_booking = Booking.objects.last()
        self.assertEqual(created_booking.student, Student.objects.get(student_id='sol_ji'))
        self.assertEqual(created_booking.room, Room.objects.get(room_id="H800-1"))
        self.assertEqual(created_booking.date, datetime.datetime.now().date())
        self.assertEqual(created_booking.start_time, datetime.time(14, 00))
        self.assertEqual(created_booking.end_time, datetime.time(15, 00))

    def testCreateCampOnTwoBooking(self):

        # Setup a second Booking right after the first one
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(student=self.student,
                               room=self.room, 
                               date=self.date,
                               start_time=self.end_time,
                               end_time=second_end_time)
        second_booking.save()

        request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "15:00"
                                    },
                                    format="json")

        force_authenticate(request, user=User.objects.get(username="solji"))
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_campon = CampOn.objects.last()
        self.assertEqual(created_campon.student, Student.objects.get(student_id='sol_ji'))
        self.assertEqual(created_campon.booking, Booking.objects.get(id=1))
        self.assertEqual(created_campon.start_time, datetime.time(12, 20))
        self.assertEqual(created_campon.end_time, datetime.time(15, 00))

    def testCreateCampOnNotAuthenticated(self):
        request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "15:00"
                                    },
                                    format="json")
        response = CampOnView.as_view()(request)

        # Verify none authorized request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testCreateCampOnInvalidTime(self):
        request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "11:00" # end time is smaller than start time
                                    },
                                    format="json")
        force_authenticate(request, user=User.objects.get(username="solji"))
        response = CampOnView.as_view()(request)

        # Verify none authorized request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateCampOnInvalidBooking(self):
        request = self.factory.post("/campon",
                                    {
                                        "booking": 10, # Booking id does not exist
                                        "start_time": "12:20",
                                        "end_time": "11:00"
                                    },
                                    format="json")
        force_authenticate(request, user=User.objects.get(username="solji"))
        response = CampOnView.as_view()(request)

        # Verify none authorized request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateCampOnWithSameBooking(self):

        # First CampOn
        first_request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:20",
                                        "end_time": "14:00"
                                    },
                                    format="json")

        force_authenticate(first_request, user=User.objects.get(username="solji"))
        first_response = CampOnView.as_view()(first_request)

        # Verify the first CampOn response status code
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        # Second CampOn with different start time
        second_request = self.factory.post("/campon",
                                    {
                                        "booking": 1,
                                        "start_time": "12:30",
                                        "end_time": "14:00"
                                    },
                                    format="json")

        force_authenticate(second_request, user=User.objects.get(username="solji"))
        second_response = CampOnView.as_view()(second_request)

        # Verify the second CampOn response status code
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
