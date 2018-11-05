from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
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

        booker = Booker(booker_id="j_lenn")
        booker.user = self.user
        booker.save()

        room1 = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        room1.save()

        room2 = Room(room_id="H833-03", capacity=8, number_of_computers=2)
        room2.save()

        booking = Booking(booker=booker, room=room1, date="2018-10-22", start_time="12:00", end_time="16:00")
        booking.save()

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
        request = self.factory.get("/room",
                                   {
                                       "room_id": '',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testRoomDeleteInvalidRoomIdNegativeId(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '-99',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testRoomDeleteValidRoomId(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '19',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testRoomUpdateRoomInvalidRoomIdNoRoomId(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testRoomUpdateRoomInvalidRoomIdNegativeId(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '-99',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testRoomUpdateRoomValidRoomId(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '20',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testRoomUpdateValidNumberOfComputers(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '21',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testRoomUpdateNumberOfComputersInvalidNumberOfComputersNegativeNumber(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '22',
                                       "capacity": '4',
                                       "number_of_computers": '-1'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testRoomUpdateNumberOfComputersInvalidNumberOfComputersNoNumber(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '22',
                                       "capacity": '4',
                                       "number_of_computers": '-1'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testUpdateCapacityValidCapacity(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '24',
                                       "capacity": '4',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testUpdateCapacityInvalidCapacityNegativeNumber(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '25',
                                       "capacity": '-1',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testUpdateCapacityInvalidCapacityNoNumber(self):
        request = self.factory.get("/room",
                                   {
                                       "room_id": '25',
                                       "capacity": '',
                                       "number_of_computers": '2'
                                   }, format="json")
        response = RoomView.as_view()(request)

        error_msg = "Invalid room. Please provide an existing room"

        self.assertEqual(response.data, error_msg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
