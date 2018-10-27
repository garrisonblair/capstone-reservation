from django.test import TestCase

from apps.rooms.models.Room import Room
from ..models.bookingExporterModels import ExternalRoomID


class TestModels(TestCase):

    def testExternalRoomIDCreation(self):

        room = Room(room_id="Room 1")
        room.save()

        external_room_id = ExternalRoomID(external_id="_ROOM1_", room=room)

        self.assertEqual(room.externalroomid, external_room_id)
