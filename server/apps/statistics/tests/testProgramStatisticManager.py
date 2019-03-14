from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.rooms.models.Room import Room
from datetime import timedelta
from apps.accounts.models.User import User
from apps.accounts.models.BookerProfile import BookerProfile
from apps.statistics.util.ProgramStatisticManager import ProgramStatisticManager
import datetime
import pdb


class TestRoomStatisticManager(TestCase):
    def setUp(self):
        self.booker1 = User.objects.create_user(username="j_corbin",
                                                email="jcorbin@email.com",
                                                password="safe_password")
        self.booker1.save()
        self.booker1.bookerprofile.program = "cse"
        self.booker1.bookerprofile.graduate_level = "ugrad"
        self.booker1.bookerprofile.save()
        self.booker1.save()

        self.booker2 = User.objects.create_user(username="j_cena",
                                                email="jcena@email.com",
                                                password="safe_password")
        self.booker2.save()
        self.booker2.bookerprofile.program = "miae"
        self.booker2.bookerprofile.graduate_level = "mthesis"
        self.booker2.bookerprofile.save()
        self.booker2.save()

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

        booking1 = Booking(booker=self.booker1,
                           room=self.room,
                           date=self.date1,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking1.save()

        booking2 = Booking(booker=self.booker1,
                           room=self.room,
                           date=self.date2,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking2.save()

        booking3 = Booking(booker=self.booker2,
                           room=self.room,
                           date=self.date3,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking3.save()

        self.stats = ProgramStatisticManager()

    def testGetPrograms(self):
        programs = self.stats.get_programs()
        self.assertEqual(programs.count(), 2)
        self.assertEqual(programs[0]['program'], 'cse')
        self.assertEqual(programs[1]['program'], 'miae')

    def testGetGradLevels(self):
        grad_levels = self.stats.get_grad_levels()
        self.assertEqual(grad_levels.count(), 2)
        self.assertEqual(grad_levels[0]['graduate_level'], 'ugrad')
        self.assertEqual(grad_levels[1]['graduate_level'], 'mthesis')

    def testGetNumProgramBookings(self):
        self.assertEqual(self.stats.get_num_program_bookings(program="cse"), 2)
        self.assertEqual(self.stats.get_num_program_bookings(program="cse", start_date=self.date2), 1)
        self.assertEqual(self.stats.get_num_program_bookings(program="miae"), 1)

        self.assertEqual(self.stats.get_num_program_bookings(grad_level="ugrad"), 2)
        self.assertEqual(self.stats.get_num_program_bookings(program="cse", grad_level="mthesis"), 0)

    def testRoomTimeBooked(self):
        self.assertEqual(self.stats.get_time_booked(program="cse"), timedelta(hours=4))
        self.assertEqual(self.stats.get_time_booked(program="miae"), timedelta(hours=2))

    def testGetAverageBookingsPerDay(self):
        date4 = datetime.datetime(2018, 12, 24).date()
        booking4 = Booking(booker=self.booker1,
                           room=self.room,
                           date=date4,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking4.save()

        date5 = datetime.datetime(2019, 1, 10).date()
        booking5 = Booking(booker=self.booker1,
                           room=self.room,
                           date=date5,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking5.save()

        self.assertEqual(self.stats.get_average_bookings_per_day(program="cse", start_date=date4, end_date=date5),
                         0.222)

    def testGetAverageTimeBookedPerDay(self):
        date4 = datetime.datetime(2018, 12, 24).date()
        booking4 = Booking(booker=self.booker1,
                           room=self.room,
                           date=date4,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking4.save()

        date5 = datetime.datetime(2019, 1, 10).date()
        booking5 = Booking(booker=self.booker1,
                           room=self.room,
                           date=date5,
                           start_time=self.start_time,
                           end_time=self.end_time)
        booking5.save()

        self.assertEqual(self.stats.get_average_time_booked_per_day(program="cse", start_date=date4, end_date=date5),
                         0.444)
