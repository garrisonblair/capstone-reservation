from django.test import TestCase

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from apps.rooms.models.Room import Room
from apps.rooms.models.RoomUnavailability import RoomUnavailability


class TestRoomUnavailability(TestCase):

    def setUp(self):
        self.today = timezone.now()
        self.tomorrow = timezone.now() + timedelta(1)

        name = "Room 1"
        capacity = 7
        number_of_computers = 2

        self.room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

    def tearDown(self):
        pass

    def testRoomUnavailabilityCreation(self):
        unavailability = RoomUnavailability(room=self.room, start_time=self.today, end_time=self.tomorrow)
        unavailability.save()

        unavailabilities = RoomUnavailability.objects.filter(room=self.room)

        self.assertEqual(unavailabilities.count(), 1)

    def testRoomUnavailabilityCreationWithNoStartTime(self):
        unavailability = RoomUnavailability(room=self.room, end_time=self.tomorrow)
        with self.assertRaises(ValidationError):
            unavailability.save()

    def testRoomUnavailabilityCreationWithNoEndTime(self):
        unavailability = RoomUnavailability(room=self.room, start_time=self.tomorrow)
        with self.assertRaises(ValidationError):
            unavailability.save()

    def testRoomUnavailabilityCreationStartTimeLaterThanEndTime(self):
        unavailability = RoomUnavailability(room=self.room, start_time=self.tomorrow, end_time=self.today)
        with self.assertRaises(ValidationError):
            unavailability.save()

    def testRoomUnavailabilityCreationSameTime(self):
        unavailability = RoomUnavailability(room=self.room, start_time=self.today, end_time=self.today)
        with self.assertRaises(ValidationError):
            unavailability.save()
