from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room

from ..views.room import RoomView


class RoomAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        room1 = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        room1.save()

        room2 = Room(room_id="H833-03", capacity=8, number_of_computers=2)
        room2.save()

    def testGetAllRooms(self):
        request = self.factory.get("/room")

        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

