from django.test import TestCase

from apps.rooms.models.Room import Room


class TestRoom(TestCase):

    def setUp(self):
        pass

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
        room_str = "Room 1, Capacity: 7, Number of computers: 2, " \
                   "Available: True, Unavailable_start_time: None, Unavailable_end_time: None"

        self.assertEqual(room_str, read_room.__str__())
