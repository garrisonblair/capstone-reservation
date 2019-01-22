from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory

from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from apps.accounts.models.User import User
from apps.statistics.util.RoomStatisticManager import RoomStatisticManager
import datetime

from apps.statistics.views.room_statistics import RoomStatistics


class TestRoomStatisticManager(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.booker = User.objects.create_user(username="j_corbin",
                                               email="jcorbin@email.com",
                                               password="safe_password")
        self.booker.user = None
        self.booker.save()

        self.user = User.objects.create_user(username='paul',
                                             email='pmcartney@beatles.com',
                                             password='yellow submarine')
        self.user.is_superuser = True
        self.user.save()

        self.room1 = Room(name="1", capacity=2, number_of_computers=1)
        self.room1.save()

        self.room2 = Room(name="2", capacity=5, number_of_computers=2)
        self.room2.save()

        self.start_time = datetime.datetime(2019, 1, 1, 12, 00).time()
        self.end_time = datetime.datetime(2019, 1, 1, 14, 00).time()

        self.date1 = datetime.datetime(2019, 1, 1).date()
        self.date2 = datetime.datetime(2019, 1, 2).date()
        self.date3 = datetime.datetime(2019, 1, 3).date()
        self.date4 = datetime.datetime(2018, 12, 24).date()
        self.date5 = datetime.datetime(2019, 1, 10).date()

        self.booking1 = Booking(booker=self.booker,
                                room=self.room1,
                                date=self.date1,
                                start_time=self.start_time,
                                end_time=self.end_time)
        self.booking1.save()

        self.booking2 = Booking(booker=self.booker,
                                room=self.room1,
                                date=self.date2,
                                start_time=self.start_time,
                                end_time=self.end_time)
        self.booking2.save()

        self.booking3 = Booking(booker=self.booker,
                                room=self.room2,
                                date=self.date3,
                                start_time=self.start_time,
                                end_time=self.end_time)
        self.booking3.save()

        self.booking4 = Booking(booker=self.booker,
                                room=self.room1,
                                date=self.date4,
                                start_time=self.start_time,
                                end_time=self.end_time)
        self.booking4.save()

        self.booking5 = Booking(booker=self.booker,
                                room=self.room2,
                                date=self.date5,
                                start_time=self.start_time,
                                end_time=self.end_time)
        self.booking5.save()

        self.stats = RoomStatisticManager()

    def testGetAllRoomStatistics(self):
        request = self.factory.get("/room_statistics?start=2018-12-24&end=2019-01-10")

        force_authenticate(request, user=User.objects.get(username="paul"))

        response = RoomStatistics.as_view()(request)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['room']["id"], 1)
        self.assertEqual(response.data[1]['room']["id"], 2)

    def testGetSingleRoomStatistics(self):
        request = self.factory.get("/room_statistics?room=1&start=2018-12-24&end=2019-01-10")

        force_authenticate(request, user=User.objects.get(username="paul"))

        response = RoomStatistics.as_view()(request)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['room']["id"], 1)
