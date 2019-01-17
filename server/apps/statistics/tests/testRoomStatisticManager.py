from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from datetime import datetime, timedelta
from apps.accounts.models.User import User
from apps.statistics.util.RoomStatisticManager import RoomStatisticManager


class TestRoomStatisticManager(TestCase):
    def setUp(self):
        self.booker = User.objects.create_user(username="j_corbin",
                                               email="jcorbin@email.com",
                                               password="safe_password")
        self.booker.user = None
        self.booker.save()

        name = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name, capacity=capacity, number_of_computers=number_of_computers)
        self.room.save()

        self.start_time = datetime(2019, 1, 1, 12, 00).time()
        self.end_time = datetime(2019, 1, 1, 14, 00).time()

        self.date1 = datetime(2019, 1, 1).date()
        self.date2 = datetime(2019, 1, 2).date()
        self.date3 = datetime(2019, 1, 3).date()

        booking1 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date1,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking1.save()

        booking2 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date2,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking2.save()

        booking3 = Booking(booker=self.booker,
                           room=self.room,
                           date=self.date3,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking3.save()

        self.stats = RoomStatisticManager()

    def testGetNumRoomBookings(self):
        self.assertEqual(self.stats.get_num_room_bookings(room=self.room), 3)
        self.assertEqual(self.stats.get_num_room_bookings(room=self.room, start_date=self.date2), 2)
        self.assertEqual(self.stats.get_num_room_bookings(room=self.room, end_date=self.date2), 2)
        self.assertEqual(
            self.stats.get_num_room_bookings(room=self.room, start_date=self.date2, end_date=self.date2),
            1)

    def testRoomTimeBooked(self):
        self.assertEqual(self.stats.get_time_booked(room=self.room), timedelta(hours=6))
        self.assertEqual(self.stats.get_time_booked(room=self.room, start_date=self.date2), timedelta(hours=4))
        self.assertEqual(self.stats.get_time_booked(room=self.room, end_date=self.date2), timedelta(hours=4))
        self.assertEqual(
            self.stats.get_time_booked(room=self.room, start_date=self.date2, end_date=self.date2),
            timedelta(hours=2))
