import datetime

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from apps.accounts.models.Booker import Booker
from apps.rooms.models.Room import Room
from ..models.Booking import Booking
from ..models.CampOn import CampOn
from ..views.campon import CampOnView
from utils.mock_datetime import mock_datetime


class CampOnAPITest(TestCase):
    def setUp(self):
        # Setup one Booking
        sid = '12345678'
        self.booker = Booker(booker_id=sid)
        self.booker.user = None
        self.booker.save()

        rid = "H800-1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(room_id=rid,
                         capacity=capacity,
                         number_of_computers=number_of_computers)
        self.room.save()

        self.date = datetime.datetime.now().today().date()
        self.start_time = datetime.datetime.strptime("12:00", "%H:%M").time()
        self.end_time = datetime.datetime.strptime("14:00", "%H:%M").time()

        self.booking = Booking(booker=self.booker,
                               room=self.room,
                               date=self.date,
                               start_time=self.start_time,
                               end_time=self.end_time)
        self.booking.save()

        # Setup one user for testing CampOn
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='sol_ji',
                                             email='solji@exid.com',
                                             password='kingmask')
        self.user.save()

        # Setup one booker for the user
        self.booker = Booker(booker_id="sol_ji")
        self.booker.user = self.user
        self.booker.save()

    # CampOn start time should be the current time. However,
    # the current time cannot be used in the test, otherwise, the test will fail if it runs at invalid period
    # So the start time in this test will be assigned values
    def testCreateCampOnSuccess(self):
        request = self.factory.post("/campon", {
                "camped_on_booking": 1,
                "end_time": "14:00"
            },
            format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))

        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_camp_on = CampOn.objects.last()

        self.assertEqual(created_camp_on.booker, Booker.objects.get(booker_id='sol_ji'))
        self.assertEqual(created_camp_on.camped_on_booking, Booking.objects.get(id=1))
        self.assertEqual(created_camp_on.start_time, datetime.time(12, 30))

        self.assertEqual(created_camp_on.end_time, datetime.time(14, 00))

    def testCreateCampOnWithBooking(self):
        request = self.factory.post("/campon", {
            "camped_on_booking": 1,
            "end_time": "15:00"
        }, format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))

        # using 12:28 to test rounding
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 28, 0, 0), datetime):
            response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_camp_on = CampOn.objects.last()

        self.assertEqual(created_camp_on.booker, Booker.objects.get(booker_id='sol_ji'))
        self.assertEqual(created_camp_on.camped_on_booking, Booking.objects.get(id=1))
        self.assertEqual(created_camp_on.start_time, datetime.time(12, 30))

        self.assertEqual(created_camp_on.end_time, datetime.time(14, 00))

        # Verify number of Booking
        self.assertEqual(len(Booking.objects.all()), 2)

        # Verify the content of the created Booking
        created_booking = Booking.objects.last()
        self.assertEqual(created_booking.booker, Booker.objects.get(booker_id='sol_ji'))
        self.assertEqual(created_booking.room, Room.objects.get(room_id="H800-1"))
        self.assertEqual(created_booking.date, datetime.datetime.now().date())
        self.assertEqual(created_booking.start_time, datetime.time(14, 00))
        self.assertEqual(created_booking.end_time, datetime.time(15, 00))

    # @unittest.skip("tests to be changed to account for actual time")
    def testCreateCampOnSecondBooking(self):
        # Setup a second Booking right after the first one
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        request = self.factory.post("/campon", {
            "camped_on_booking": 1,
            "end_time": "15:00"
        }, format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCreateCampOnNotAuthenticated(self):
        request = self.factory.post("/campon", {
            "camped_on_booking": 1,
            "end_time": "15:00"
        }, format="json")
        response = CampOnView.as_view()(request)

        # Verify none authorized request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testCreateCampOnInvalidBooking(self):
        request = self.factory.post("/campon", {
            "camped_on_booking": 10,  # Booking id does not exist
            "end_time": "11:00"
        }, format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))
        response = CampOnView.as_view()(request)

        # Verify none authorized request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testGetOneCampOnById(self):
        # Setup a second booking
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        # Setup two CampOns
        start_time_1 = datetime.datetime.strptime("12:20", "%H:%M").time()
        end_time_1 = datetime.datetime.strptime("13:00", "%H:%M").time()
        camp_on_1 = CampOn(booker=self.booker,
                           camped_on_booking=self.booking,
                           start_time=start_time_1,
                           end_time=end_time_1)
        camp_on_1.save()
        start_time_2 = datetime.datetime.strptime("14:00", "%H:%M").time()
        end_time_2 = datetime.datetime.strptime("15:00", "%H:%M").time()
        camp_on_2 = CampOn(booker=self.booker,
                           camped_on_booking=second_booking,
                           start_time=start_time_2,
                           end_time=end_time_2)
        camp_on_2.save()
        self.assertEqual(len(CampOn.objects.all()), 2)

        request = self.factory.get("/campon", {
            "id": 1
        }, format="json")

        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 1)

    def testGetCampOnByBooking(self):
        # Setup a second booking
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        # Setup two CampOns
        start_time_1 = datetime.datetime.strptime("12:20", "%H:%M").time()
        end_time_1 = datetime.datetime.strptime("13:00", "%H:%M").time()
        camp_on_1 = CampOn(booker=self.booker,
                           camped_on_booking=self.booking,
                           start_time=start_time_1,
                           end_time=end_time_1)
        camp_on_1.save()
        start_time_2 = datetime.datetime.strptime("14:00", "%H:%M").time()
        end_time_2 = datetime.datetime.strptime("15:00", "%H:%M").time()
        camp_on_2 = CampOn(booker=self.booker,
                           camped_on_booking=second_booking,
                           start_time=start_time_2,
                           end_time=end_time_2)
        camp_on_2.save()
        self.assertEqual(len(CampOn.objects.all()), 2)

        request = self.factory.get("/campon", {
            "camped_on_booking": 1
        }, format="json")

        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 1)

    def testGetCampOnByBookingAndTime(self):
        # Setup a second booking
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        # Setup two CampOns
        start_time_1 = datetime.datetime.strptime("12:20", "%H:%M").time()
        end_time_1 = datetime.datetime.strptime("13:00", "%H:%M").time()
        camp_on_1 = CampOn(booker=self.booker,
                           camped_on_booking=self.booking,
                           start_time=start_time_1,
                           end_time=end_time_1)
        camp_on_1.save()
        start_time_2 = datetime.datetime.strptime("14:00", "%H:%M").time()
        end_time_2 = datetime.datetime.strptime("15:00", "%H:%M").time()
        camp_on_2 = CampOn(booker=self.booker,
                           camped_on_booking=second_booking,
                           start_time=start_time_2,
                           end_time=end_time_2)
        camp_on_2.save()
        self.assertEqual(len(CampOn.objects.all()), 2)

        request = self.factory.get("/campon", {
            "camped_on_booking": 1,
            "start_time": "12:20",
            "end_time": "13:00"
        }, format="json")

        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 1)

    def testGetCampOnByTime(self):
        # Setup a second booking
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        # Setup two CampOns
        start_time_1 = datetime.datetime.strptime("12:20", "%H:%M").time()
        end_time_1 = datetime.datetime.strptime("13:00", "%H:%M").time()
        camp_on_1 = CampOn(booker=self.booker,
                           camped_on_booking=self.booking,
                           start_time=start_time_1,
                           end_time=end_time_1)
        camp_on_1.save()
        start_time_2 = datetime.datetime.strptime("14:00", "%H:%M").time()
        end_time_2 = datetime.datetime.strptime("15:00", "%H:%M").time()
        camp_on_2 = CampOn(booker=self.booker,
                           camped_on_booking=second_booking,
                           start_time=start_time_2,
                           end_time=end_time_2)
        camp_on_2.save()
        self.assertEqual(len(CampOn.objects.all()), 2)

        request = self.factory.get("/campon", {
            "start_time": "12:20",
            "end_time": "13:00"
        }, format="json")

        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 1)

    def testGetAllCampOn(self):
        # Setup a second booking
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        # Setup two CampOns
        start_time_1 = datetime.datetime.strptime("12:20", "%H:%M").time()
        end_time_1 = datetime.datetime.strptime("13:00", "%H:%M").time()
        CampOn.objects.create(booker=self.booker,
                              camped_on_booking=self.booking,
                              start_time=start_time_1,
                              end_time=end_time_1)

        start_time_2 = datetime.datetime.strptime("14:00", "%H:%M").time()
        end_time_2 = datetime.datetime.strptime("15:00", "%H:%M").time()

        CampOn.objects.create(booker=self.booker,
                              camped_on_booking=second_booking,
                              start_time=start_time_2,
                              end_time=end_time_2)

        self.assertEqual(len(CampOn.objects.all()), 2)

        request = self.factory.get("/campon", {
        }, format="json")

        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 2)

    def testGetCampOnNotFound(self):
        # Setup a second booking
        second_end_time = datetime.datetime.strptime("16:00", "%H:%M").time()
        second_booking = Booking(booker=self.booker,
                                 room=self.room,
                                 date=self.date,
                                 start_time=self.end_time,
                                 end_time=second_end_time)
        second_booking.save()

        # Setup two CampOns
        start_time_1 = datetime.datetime.strptime("12:20", "%H:%M").time()
        end_time_1 = datetime.datetime.strptime("13:00", "%H:%M").time()
        camp_on_1 = CampOn(booker=self.booker,
                           camped_on_booking=self.booking,
                           start_time=start_time_1,
                           end_time=end_time_1)
        camp_on_1.save()
        start_time_2 = datetime.datetime.strptime("14:00", "%H:%M").time()
        end_time_2 = datetime.datetime.strptime("15:00", "%H:%M").time()
        camp_on_2 = CampOn(booker=self.booker,
                           camped_on_booking=second_booking,
                           start_time=start_time_2,
                           end_time=end_time_2)
        camp_on_2.save()
        self.assertEqual(len(CampOn.objects.all()), 2)

        request = self.factory.get("/campon", {
            "id": 10,
        },
                                   format="json")
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 0)

    def testGetEmptyCampOn(self):
        request = self.factory.get("/campon", {
        }, format="json")

        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_camp_on = response.data
        self.assertEqual(len(retrieved_camp_on), 0)

    def testGetCampOnWithInvalidCampOnId(self):
        request = self.factory.get("/campon", {
            "id": str
        }, format="json")
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testGetCampOnWithInvalidBookingId(self):
        request = self.factory.get("/campon", {
            "camped_on_booking": str
        }, format="json")
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testGetCampOnWithInvalidStartTime(self):
        request = self.factory.get("/campon", {
            "start_time": "str",
            "end_time": self.end_time,
        }, format="json")
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testGetCampOnWithInvalidEndTime(self):
        request = self.factory.get("/campon", {
            "start_time": self.start_time,
            "end_time": str,
        }, format="json")
        response = CampOnView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
