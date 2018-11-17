from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking

from ..views.room import RoomList
from ..views.room import RoomCreate
from ..views.room import RoomRetrieveUpdateDestroy


class RoomAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.is_superuser = True
        self.user.save()

        self.booker = Booker(booker_id="j_lenn")
        self.booker.user = self.user
        self.booker.save()

        self.room1 = Room(id=1,
                          name="H833-17",
                          capacity=4,
                          number_of_computers=1)

        self.room1.save()

        self.room2 = Room(id=2,
                          name="H833-03",
                          capacity=8,
                          number_of_computers=2)
        self.room2.save()

        self.booking = Booking(booker=self.booker,
                               room=self.room1,
                               date="2018-10-22",
                               start_time="12:00",
                               end_time="16:00")
        self.booking.save()

    def testGetAllRooms(self):
        request = self.factory.get("/rooms")

        response = RoomList.as_view()(request)
        response_data = [
            {
                "id": 1,
                "name": "H833-17",
                "capacity": 4,
                "number_of_computers": 1
            },
            {
                "id": 2,
                "name": "H833-03",
                "capacity": 8,
                "number_of_computers": 2
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def testGetRoomsAtDateTime(self):
        request = self.factory.get("/rooms",
                                   {
                                       "start_date_time": '2018-10-22 11:00',
                                       "end_date_time": '2018-10-22 17:00'
                                   }, format="json")

        response = RoomList.as_view()(request)
        response_data = [
            {
                "id": 2,
                "name": "H833-03",
                "capacity": 8,
                "number_of_computers": 2
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def testGetRoomsInvalidRequestEndBeforeStart(self):
        request = self.factory.get("/rooms",
                                   {
                                       "start_date_time": '2018-10-22 17:00',
                                       "end_date_time": '2018-10-22 11:00'
                                   }, format="json")  # start time after end time

        force_authenticate(request, user=User.objects.get(username="john"))

        response = RoomList.as_view()(request)

        error_msg = "Invalid times: start time must be before end time"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testGetRoomsInvalidRequestMissingLastParam(self):
        request = self.factory.get("/rooms",
                                   {
                                       "start_date_time": '2018-10-22 11:00'
                                   }, format="json")

        response = RoomList.as_view()(request)

        force_authenticate(request, user=User.objects.get(username="john"))

        error_msg = "Invalid times: please supply a start time and an end time"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testGetRoomsInvalidRequestMissingFirstParam(self):
        request = self.factory.get("/rooms",
                                   {
                                       "end_date_time": '2018-10-22 17:00'
                                   }, format="json")

        response = RoomList.as_view()(request)

        error_msg = "Invalid times: please supply a start time and an end time"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testGetRoomsInvalidRequestWrongParameterFormat(self):
        request = self.factory.get("/rooms",
                                   {
                                       "start_date_time": 'AdhG4gf',
                                       "end_date_time": '1234'
                                   }, format="json")

        response = RoomList.as_view()(request)

        error_msg = "Invalid parameters, please input parameters in the YYYY-MM-DD HH:mm format"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testRoomDeleteInvalidRoomIdNonExistentId(self):

        request = self.factory.delete("/room",
                                      {
                                         "id": -99
                                      }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        instances_of_deleted_room_before = len(Room.objects.filter(id='-99'))

        response = RoomRetrieveUpdateDestroy.as_view()(request, pk='-99')

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        instances_of_deleted_room_after = len(Room.objects.filter(name=self.room1.name))

        self.assertEqual(instances_of_deleted_room_before+1, instances_of_deleted_room_after)

    def testRoomDeleteValidExistingRoomId(self):
        request = self.factory.delete("/room",
                                      {
                                         "id": self.room1.id
                                      }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomRetrieveUpdateDestroy.as_view()(request, pk=self.room1.id)
        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after + 1)

        instances_of_deleted_room = len(Room.objects.filter(name=self.room1.name))

        self.assertEqual(instances_of_deleted_room, 0)

    def testRoomUpdateRoomInValidRoomIdNoRoomId(self):
        request = self.factory.patch("/room",
                                     {
                                        "id": self.room1.id,
                                        "name": ''
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomRetrieveUpdateDestroy.as_view()(request, pk=self.room1.id)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

    def testRoomCreateRoomValidNewRoomId(self):
        request = self.factory.post("/room",
                                    {
                                        "name": 'H833-100',
                                        "capacity": 4,
                                        "number_of_computers": 2
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomCreate.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number_of_rooms_before + 1, number_of_rooms_after)

        room = Room.objects.get(name='H833-100')

        self.assertEqual(room.name, 'H833-100')
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 2)

    def testRoomUpdateValidNumberOfComputers(self):
        request = self.factory.patch("/room",
                                     {
                                        "id": self.room1.id,
                                        "number_of_computers": 2
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = response = RoomRetrieveUpdateDestroy.as_view()(request, pk=self.room1.id)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(name=self.room1.name)

        self.assertEqual(room.name, self.room1.name)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 2)

    def testUpdateCapacityValidCapacity(self):
        request = self.factory.patch("/room",
                                     {
                                        "id": self.room1.id,
                                        "capacity": 4
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomRetrieveUpdateDestroy.as_view()(request, pk=self.room1.id)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(id=self.room1.id)

        self.assertEqual(room.name, self.room1.name)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, self.room1.number_of_computers)

    def testUpdateCapacityInvalidCapacityNoNumber(self):
        request = self.factory.patch("/room",
                                     {
                                        "id": self.room1.id,
                                        "capacity": ''
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomRetrieveUpdateDestroy.as_view()(request, pk=self.room1.id)
        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(id=self.room1.id)

        self.assertEqual(room.name, self.room1.name)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

    def testUpdateRoomAuthorizationFail(self):
        request = self.factory.patch("/room",
                                     {
                                        "id": self.room1.id,
                                        "name": self.room1.id
                                     }, format="json")

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomRetrieveUpdateDestroy.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(id=self.room1.id)

        self.assertEqual(room.name, self.room1.name)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

    def testDeleteRoomAuthorizationFail(self):
        request = self.factory.delete("/room",
                                      {
                                        "id": self.room1.id
                                      }, format="json")

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        instances_of_deleted_room_before = len(Room.objects.filter(id=self.room1.id))

        response = RoomRetrieveUpdateDestroy.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(id=self.room1.id)

        self.assertEqual(room.name, self.room1.name)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

        instances_of_deleted_room_after = len(Room.objects.filter(id=self.room1.id))

        self.assertEqual(instances_of_deleted_room_before, instances_of_deleted_room_after)
