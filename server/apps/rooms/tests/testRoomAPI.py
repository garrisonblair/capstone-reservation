from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking

from ..views.room import RoomView, RoomDeleteView, RoomCreateView, RoomUpdateView


class RoomAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glass onion')
        self.user.save()

        self.booker = Booker(booker_id="j_lenn")
        self.booker.user = self.user
        self.booker.save()

        self.room1 = Room(room_id="H833-17",
                          capacity=4,
                          number_of_computers=1)

        self.room1.save()

        self.room2 = Room(room_id="H833-03",
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
        request = self.factory.get("/room")

        response = RoomView.as_view()(request)
        response_data = [
            {
                "id": 1,
                "room_id": "H833-17",
                "capacity": 4,
                "number_of_computers": 1
            },
            {
                "id": 2,
                "room_id": "H833-03",
                "capacity": 8,
                "number_of_computers": 2
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def testGetRoomsAtDateTime(self):
        request = self.factory.get("/room",
                                   {
                                       "start_date_time": '2018-10-22 11:00',
                                       "end_date_time": '2018-10-22 17:00'
                                   }, format="json")

        response = RoomView.as_view()(request)
        response_data = [
            {
                "id": 2,
                "room_id": "H833-03",
                "capacity": 8,
                "number_of_computers": 2
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    def testGetRoomsInvalidRequestEndBeforeStart(self):
        request = self.factory.get("/room",
                                   {
                                       "start_date_time": '2018-10-22 17:00',
                                       "end_date_time": '2018-10-22 11:00'
                                   }, format="json")  # start time after end time

        force_authenticate(request, user=User.objects.get(username="john"))

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

        force_authenticate(request, user=User.objects.get(username="john"))

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

    def testGetRoomsInvalidRequestWrongParameterFormat(self):
        request = self.factory.get("/room",
                                   {
                                       "start_date_time": 'AdhG4gf',
                                       "end_date_time": '1234'
                                   }, format="json")

        response = RoomView.as_view()(request)

        error_msg = "Invalid parameters, please input parameters in the YYYY-MM-DD HH:mm format"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)

    def testRoomDeleteInvalidRoomIdNoRoomId(self):

        request = self.factory.delete("/room",
                                      {
                                         "room_id": ''
                                      }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomDeleteView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, error_msg)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

    def testRoomDeleteInvalidRoomIdNonExistentId(self):

        request = self.factory.delete("/room",
                                      {
                                         "room_id": '-99'
                                      }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        instances_of_deleted_room_before = len(Room.objects.filter(room_id='-99'))

        response = RoomDeleteView.as_view()(request, room_id='-99')

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        instances_of_deleted_room_after = len(Room.objects.filter(room_id=self.room1.room_id))

        self.assertEqual(instances_of_deleted_room_before+1, instances_of_deleted_room_after)

    def testRoomDeleteValidExistingRoomId(self):
        request = self.factory.delete("/room",
                                      {
                                         "room_id": self.room1.room_id
                                      }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomDeleteView.as_view()(request, room_id=self.room1.room_id)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after + 1)

        instances_of_deleted_room = len(Room.objects.filter(room_id=self.room1.room_id))

        self.assertEqual(instances_of_deleted_room, 0)

    def testRoomUpdateRoomInValidRoomIdNoRoomId(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": '',
                                        "capacity": 4,
                                        "number_of_computers": 2
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

    def testRoomCreateRoomValidNewRoomId(self):
        request = self.factory.post("/room",
                                    {
                                        "room_id": 'H833-99',
                                        "capacity": 4,
                                        "number_of_computers": 2
                                    }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomCreateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number_of_rooms_before + 1, number_of_rooms_after)

        room = Room.objects.get(room_id='H833-99')

        self.assertEqual(room.room_id, 'H833-99')
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 2)

    def testRoomUpdateValidNumberOfComputers(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id,
                                        "capacity": 4,
                                        "number_of_computers": 2
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 2)

    def testRoomUpdateNumberOfComputersInvalidNumberOfComputersNegativeNumber(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id,
                                        "capacity": 4,
                                        "number_of_computers": -1
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request, room_id=self.room1.room_id, number_of_computers=-1)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, self.room1.number_of_computers)

    def testRoomUpdateNumberOfComputersInvalidNumberOfComputersNoNumber(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id,
                                        "capacity": 4,
                                        "number_of_computers": -1
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, self.room1.number_of_computers)

    def testUpdateCapacityValidCapacity(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id,
                                        "capacity": 4,
                                        "number_of_computers": 2
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 2)

    def testUpdateCapacityInvalidCapacityNegativeNumber(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id,
                                        "capacity": -1,
                                        "number_of_computers": 2
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

    def testUpdateCapacityInvalidCapacityNoNumber(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id,
                                        "capacity": '',
                                        "number_of_computers": 2
                                     }, format="json")

        force_authenticate(request, user=User.objects.get(username="john"))

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

    def testUpdateRoomAuthorizationFail(self):
        request = self.factory.patch("/room",
                                     {
                                        "room_id": self.room1.room_id
                                     }, format="json")

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

    def testDeleteRoomAuthorizationFail(self):
        request = self.factory.delete("/room",
                                      {
                                          "room_id": self.room1.room_id
                                      }, format="json")

        rooms_before = Room.objects.all()
        number_of_rooms_before = len(rooms_before)

        instances_of_deleted_room_before = len(Room.objects.filter(room_id=self.room1.room_id))

        response = RoomUpdateView.as_view()(request)

        rooms_after = Room.objects.all()
        number_of_rooms_after = len(rooms_after)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(number_of_rooms_before, number_of_rooms_after)

        room = Room.objects.get(room_id=self.room1.room_id)

        self.assertEqual(room.room_id, self.room1.room_id)
        self.assertEqual(room.capacity, 4)
        self.assertEqual(room.number_of_computers, 1)

        instances_of_deleted_room_after = len(Room.objects.filter(room_id=self.room1.room_id))

        self.assertEqual(instances_of_deleted_room_before, instances_of_deleted_room_after)
