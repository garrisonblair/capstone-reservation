from django.test import TestCase
from apps.booking.models.Booking import Booking
from apps.booking.models.CampOn import CampOn
from apps.accounts.models.User import User
from apps.rooms.models.Room import Room
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class TestCampOn(TestCase):
    def setUp(self):
        # Setup one booker
        sid = '12345678'
        self.booker = User.objects.create_user(username="f_daigl",
                                               email="fred@email.com",
                                               password="passw0rd")
        self.booker.save()

        # Create a second booker for camp-on
        booker_id = '87654321'
        self.campbooker = User.objects.create_user(username="j_lenn",
                                                   email="john@beatles.com",
                                                   password="password")
        self.campbooker.save()

        # Setup one Room
        name = "1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name,
                         capacity=capacity,
                         number_of_computers=number_of_computers)
        self.room.save()

        # Setup one Date and Time
        self.date = datetime.now().today().date()
        self.start_time = datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.strptime("14:00", "%H:%M").time()

        # Setup one Booking
        self.booking = Booking(booker=self.booker,
                               room=self.room,
                               date=self.date,
                               start_time=self.start_time,
                               end_time=self.end_time)
        self.booking.save()

    def testCampOnCreation(self):
        # Get the current time

        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("12:15", "%H:%M").time()
        camp_on = CampOn.objects.create(booker=self.campbooker,
                                        camped_on_booking=self.booking,
                                        start_time=camp_on_start_time,
                                        end_time=self.end_time)

        read_camp_on = CampOn.objects.get(booker=self.campbooker,
                                          camped_on_booking=self.booking,
                                          start_time=camp_on_start_time,
                                          end_time=self.end_time)
        self.assertEqual(read_camp_on, camp_on)
        self.assertEqual(len(CampOn.objects.all()), 1)

    def testCampOnNotToday(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("12:15", "%H:%M").time()

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_booking = Booking(booker=self.booker,
                                    room=self.room,
                                    date=yesterday,
                                    start_time=self.start_time,
                                    end_time=self.end_time)
        yesterday_booking.save()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=yesterday_booking,
                                  start_time=camp_on_start_time,
                                  end_time=self.end_time)
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCampOnEndTimeSmallerThanStartTime(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("12:15", "%H:%M").time()
        camp_on_end_time = datetime.strptime("11:00", "%H:%M").time()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=self.booking,
                                  start_time=camp_on_start_time,
                                  end_time=camp_on_end_time)
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCampOnSamebookerOnSameBooking(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("12:15", "%H:%M").time()
        CampOn.objects.create(booker=self.campbooker,
                              camped_on_booking=self.booking,
                              start_time=camp_on_start_time,
                              end_time=self.end_time)

        camp_on_start_time = datetime.strptime("12:30", "%H:%M").time()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=self.booking,
                                  start_time=camp_on_start_time,
                                  end_time=self.end_time)
        self.assertEqual(len(CampOn.objects.all()), 1)

    def testCampOnStartTimeEarlierThanBooking(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("11:00", "%H:%M").time()
        camp_on_end_time = datetime.strptime("13:00", "%H:%M").time()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=self.booking,
                                  start_time=camp_on_start_time,
                                  end_time=camp_on_end_time)
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCampOnStartTimeLaterThanBooking(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("14:15", "%H:%M").time()
        camp_on_end_time = datetime.strptime("15:00", "%H:%M").time()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=self.booking,
                                  start_time=camp_on_start_time,
                                  end_time=camp_on_end_time)
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCampOnEndTimeLaterThan23PM(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("13:00", "%H:%M").time()
        camp_on_end_time = datetime.strptime("23:05", "%H:%M").time()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=self.booking,
                                  start_time=camp_on_start_time,
                                  end_time=camp_on_end_time)
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCampOnEndTimeEarlierThan8AM(self):
        # Fake the start time other than current time. Otherwise, the test will fail if it runs between 23:00-00:00
        camp_on_start_time = datetime.strptime("13:00", "%H:%M").time()
        camp_on_end_time = datetime.strptime("1:05", "%H:%M").time()

        with self.assertRaises(ValidationError):
            CampOn.objects.create(booker=self.campbooker,
                                  camped_on_booking=self.booking,
                                  start_time=camp_on_start_time,
                                  end_time=camp_on_end_time)
        self.assertEqual(len(CampOn.objects.all()), 0)
