from django.test import TestCase

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from apps.rooms.models.Room import Room


class TestRoom(TestCase):

    def setUp(self):
        self.today = timezone.now()
        self.tomorrow = timezone.now() + timedelta(1)
        self.tomorrow = self.tomorrow

    def tearDown(self):
        pass

    def testRoomCreation(self):
        name = "Room 1"
        capacity = 7
        number_of_computers = 2

        room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        room.save()

        read_room = Room.objects.all().get(name=name)

        self.assertEqual(read_room, room)

    def test__str__(self):
        name = "Room 1"
        capacity = 7
        number_of_computers = 2

        room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        room.save()

        read_room = Room.objects.all().get(name=name)
        room_str = "Room 1, Capacity: 7, Number of computers: 2"

        self.assertEqual(room_str, read_room.__str__())
