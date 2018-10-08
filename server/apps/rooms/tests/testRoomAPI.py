from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking

from ..views.room import RoomView


class RoomAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        student = Student(student_id="j_lenn")
        student.user = self.user
        student.save()

        room1 = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        room1.save()

        room2 = Room(room_id="H833-03", capacity=8, number_of_computers=2)
        room2.save()

        booking = Booking(student=student, room=room1, date="2018-10-22", start_time="12:00", end_time="16:00")
        booking.save()

    def testGetAllRooms(self):
        request = self.factory.get("/room")

        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetRoomsAtDateTime(self):
        request = self.factory.get("/room",
                                   {
                                        "start_date_time": '2018-10-22 11:00',
                                        "end_date_time": '2018-10-22 17:00'
                                   }, format="json")

        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetRoomsInvalidRequestEndBeforeStart(self):
        request = self.factory.get("/room",
                                   {
                                        "start_date_time": '2018-10-22 17:00',
                                        "end_date_time": '2018-10-22 11:00'
                                   }, format="json")  # start time after end time

        response = RoomView.as_view()(request)

        error_msg = "Invalid times: start time must be before end time"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testGetRoomsInvalidRequestMissingLastParam(self):
        request = self.factory.get("/room",
                                   {
                                        "start_date_time": '2018-10-22 11:00'
                                   }, format="json")

        response = RoomView.as_view()(request)

        error_msg = "Invalid times: please supply a start time and an end time"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testGetRoomsInvalidRequestMissingFirstParam(self):

        request = self.factory.get("/room",
                                   {
                                       "end_date_time": '2018-10-22 17:00'
                                   }, format="json")

        response = RoomView.as_view()(request)

        error_msg = "Invalid times: please supply a start time and an end time"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)
