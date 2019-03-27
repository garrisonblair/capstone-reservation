from django.test.testcases import TestCase
from apps.rooms.models.Room import Room
from apps.accounts.models.User import User
from apps.rooms.models.RoomUnavailability import RoomUnavailability
from apps.rooms.views.room_unavailability import RoomUnavailabilityList
from apps.rooms.views.room_unavailability import RoomUnavailabilityCreate
from apps.rooms.views.room_unavailability import RoomUnavailabilityRetrieveUpdateDestroy
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate


class RoomUnavailabilityAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.today = timezone.now()
        self.tomorrow = timezone.now() + timedelta(1)
        self.yesterday = timezone.now() - timedelta(1)

        self.room = Room(name="Room 1", capacity=7, number_of_computers=2)
        self.room.save()

        self.room1 = Room(name="Room 2", capacity=4, number_of_computers=1)
        self.room1.save()

        self.room2 = Room(name="Room 3", capacity=9, number_of_computers=3)
        self.room2.save()

        unavailability = RoomUnavailability(room=self.room, start_time=self.today, end_time=self.tomorrow)
        unavailability.save()

        unavailability = RoomUnavailability(room=self.room1, start_time=self.yesterday, end_time=self.today)
        unavailability.save()

        self.admin = User.objects.create_user(username='admin',
                                              email='admin@alt.com',
                                              password='admin')
        self.admin.is_superuser = True
        self.admin.save()

    def testGetAllRoomUnavilabilities(self):
        request = self.factory.get("/room_unavailabilities", {}, format="json")

        response = RoomUnavailabilityList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def testGetRoomUnavilabilitiesByRoom(self):
        params = {
            "room_id": 1
        }
        request = self.factory.get("/room_unavailabilities", params, format="json")

        response = RoomUnavailabilityList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testGetRoomUnavilabilitiesByTime(self):
        params = {
            "date_time": self.tomorrow
        }
        request = self.factory.get("/room_unavailabilities", params, format="json")

        response = RoomUnavailabilityList.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testRoomUnavilabilitiesCreation(self):
        params = {
            "room": self.room2.id,
            "start_time": self.yesterday,
            "end_time": self.tomorrow
        }
        request = self.factory.post("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoomUnavailability.objects.all().count(), 3)

    def testRoomUnavilabilitiesCreationWithNoAdmin(self):
        params = {
            "room": self.room2.id,
            "start_time": self.yesterday,
            "end_time": self.tomorrow
        }
        request = self.factory.post("/room_unavailability", params, format="json")

        response = RoomUnavailabilityCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testRoomUnavilabilitiesCreationWithNoStartTime(self):
        params = {
            "room": self.room2.id,
            "end_time": self.tomorrow
        }
        request = self.factory.post("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testRoomUnavilabilitiesCreationWithNoInvalidTime(self):
        params = {
            "room": self.room2.id,
            "start_time": "not a time",
            "end_time": self.tomorrow
        }
        request = self.factory.post("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testRoomUnavilabilitiesCreationWithNoInvalidRoom(self):
        params = {
            "room": 99999,
            "start_time": self.yesterday,
            "end_time": self.tomorrow
        }
        request = self.factory.post("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testRoomUnavilabilitiesCreationWithNoInvalidRoom(self):
        params = {
            "room": 99999,
            "start_time": self.yesterday,
            "end_time": self.tomorrow
        }
        request = self.factory.post("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testDeleteRoomUnavilability(self):
        request = self.factory.delete("/room_unavailability")

        force_authenticate(request, user=User.objects.get(username="admin"))
        response = RoomUnavailabilityRetrieveUpdateDestroy.as_view()(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RoomUnavailability.objects.all().count(), 1)

    def testDeleteRoomUnavilabilityWithNoAdmin(self):
        request = self.factory.delete("/room_unavailability")

        response = RoomUnavailabilityRetrieveUpdateDestroy.as_view()(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testUpdateRoomUnavilabilities(self):
        params = {
            "start_time": self.yesterday,
            "end_time": self.tomorrow
        }
        request = self.factory.patch("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityRetrieveUpdateDestroy.as_view()(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)

    def testUpdateRoomUnavilabilitiesWithInvalidTime(self):
        params = {
            "start_time": "not a time"
        }
        request = self.factory.patch("/room_unavailability", params, format="json")
        force_authenticate(request, user=User.objects.get(username="admin"))

        response = RoomUnavailabilityRetrieveUpdateDestroy.as_view()(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RoomUnavailability.objects.all().count(), 2)
