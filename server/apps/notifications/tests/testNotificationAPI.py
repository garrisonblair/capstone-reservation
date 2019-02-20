import datetime
from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from apps.accounts.models.User import User
from apps.booking.models.Booking import Booking
from apps.notifications.views.notification import NotificationCreate
from apps.rooms.models.Room import Room


class NotificationAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User(username="user")
        self.user.save()

        self.room1 = Room(name="Room1", capacity=1, number_of_computers=1)
        self.room1.save()
        self.booker = User(username="username")
        self.booker.save()
        self.booking1 = Booking(
            room=self.room1,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(10, 0, 0),
            end_time=datetime.time(15, 0, 0),
            booker=self.booker
        )
        self.booking1.save()
        self.booking2 = Booking(
            room=self.room1,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(15, 0, 0),
            end_time=datetime.time(17, 0, 0),
            booker=self.booker
        )
        self.booking2.save()

        self.room2 = Room(name="Room2", capacity=1, number_of_computers=1)
        self.room2.save()
        self.booking3 = Booking(
            room=self.room2,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(10, 0, 0),
            end_time=datetime.time(12, 0, 0),
            booker=self.booker
        )
        self.booking3.save()
        self.booking4 = Booking(
            room=self.room2,
            date=datetime.date(2020, 1, 1),
            start_time=datetime.time(16, 0, 0),
            end_time=datetime.time(17, 0, 0),
            booker=self.booker
        )
        self.booking4.save()

    def testNotificationCreateAvailableRoomsAPI(self):
        request = self.factory.post("/notify",
                                    {
                                        "booker": self.user.id,
                                        "rooms": [self.room1.id, self.room2.id],
                                        "date": datetime.date(2020, 1, 1),
                                        "range_start": "11:00:00",
                                        "range_end": "16:00:00",
                                        "minimum_booking_time": datetime.timedelta(hours=4)
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = NotificationCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["room"], self.room2.id)
        self.assertEqual(response.data["start_time"], datetime.time(12, 0, 0))
        self.assertEqual(response.data["end_time"], datetime.time(16, 0, 0))

    def testNotificationCreateNoAvailableRoomsAPI(self):
        request = self.factory.post("/notify",
                                    {
                                        "booker": self.user.id,
                                        "rooms": [self.room1.id],
                                        "date": datetime.date(2020, 1, 1),
                                        "range_start": "11:00:00",
                                        "range_end": "16:00:00",
                                        "minimum_booking_time": datetime.timedelta(hours=4)
                                    }, format="json")

        force_authenticate(request, user=self.user)

        response = NotificationCreate.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
