from django.test import TestCase

from apps.accounts.models.Room import Room


class TestRoom(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRoomCreation(self):
        room_id = "Room 1"
        capacity = 7
        number_of_computers = 2

        room = Room(room_id=room_id, capacity=capacity, number_of_computers=number_of_computers)
        room.save()

        read_room = Room.objects.all().get(room_id=room_id)

        self.assertEqual(read_room, room)

    def test__str__(self):
        room_id = "Room 1"
        capacity = 7
        number_of_computers = 2

        room = Room(room_id=room_id, capacity=capacity, number_of_computers=number_of_computers)
        room.save()

        read_room = Room.objects.all().get(room_id=room_id)
        room_str = "Room 1, Capacity: 7, Number of computers: 2"

        self.assertEqual(room_str, read_room.__str__())
