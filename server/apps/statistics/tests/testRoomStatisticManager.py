from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from datetime import timedelta
from apps.accounts.models.User import User
from apps.statistics.util.RoomStatisticManager import RoomStatisticManager
import datetime


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

        self.start_time = datetime.datetime(2019, 1, 1, 12, 00).time()
        self.end_time = datetime.datetime(2019, 1, 1, 14, 00).time()

        self.date1 = datetime.datetime(2019, 1, 1).date()
        self.date2 = datetime.datetime(2019, 1, 2).date()
        self.date3 = datetime.datetime(2019, 1, 3).date()

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
        self.stats.get_average_bookings_per_day(self.room)

    def testGetAverageBookingsPerDay(self):
        date4 = datetime.datetime(2018, 12, 24).date()
        booking4 = Booking(booker=self.booker,
                           room=self.room,
                           date=date4,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking4.save()

        date5 = datetime.datetime(2019, 1, 10).date()
        booking5 = Booking(booker=self.booker,
                           room=self.room,
                           date=date5,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking5.save()

        self.assertEqual(self.stats.get_average_bookings_per_day(room=self.room, start_date=date4, end_date=date5),
                         0.278)

    def testGetAverageTimeBookedPerDay(self):
        date4 = datetime.datetime(2018, 12, 24).date()
        booking4 = Booking(booker=self.booker,
                           room=self.room,
                           date=date4,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking4.save()

        date5 = datetime.datetime(2019, 1, 10).date()
        booking5 = Booking(booker=self.booker,
                           room=self.room,
                           date=date5,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking5.save()

        self.assertEqual(self.stats.get_average_time_booked_per_day(room=self.room, start_date=date4, end_date=date5),
                         0.556)

    def testGetRoomStatistics(self):
        date4 = datetime.datetime(2018, 12, 24).date()
        booking4 = Booking(booker=self.booker,
                           room=self.room,
                           date=date4,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking4.save()

        date5 = datetime.datetime(2019, 1, 10).date()
        booking5 = Booking(booker=self.booker,
                           room=self.room,
                           date=date5,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking5.save()

        stats = {'average_bookings_per_day': 0.278,
                 'average_time_booked_per_day': 0.556,
                 'hours_booked': 10.0,
                 'num_room_bookings': 5,
                 'room': {'available': True, 'number_of_computers': 2, 'capacity': 7, 'name': '1',
                          'id': 1, 'unavailable_start_time': None, 'unavailable_end_time': None}}

        self.assertEqual(self.stats.get_serialized_statistics(room=self.room, start_date=date4, end_date=date5), stats)
