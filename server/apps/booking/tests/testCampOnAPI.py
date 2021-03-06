import datetime
import json
import unittest

from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from django.contrib.admin.models import LogEntry, ContentType, ADDITION

from apps.accounts.models.User import User
from apps.rooms.models.Room import Room
from apps.booking.models.Booking import Booking
from apps.booking.models.CampOn import CampOn
from apps.booking.views.campon import CampOnList
from apps.booking.views.campon import CampOnCreate
from apps.booking.serializers.campon import CampOnSerializer, LogCampOnSerializer
from apps.booking.serializers.booking import BookingSerializer, LogBookingSerializer
from apps.util.mock_datetime import mock_datetime


class CampOnAPITest(TestCase):
    def setUp(self):
        # Setup one Booking
        self.booker = User.objects.create_user(username="f_daigl",
                                               email="fred@email.com",
                                               password="safe_password")
        self.booker.save()

        name = "H800-1"
        capacity = 7
        number_of_computers = 2
        self.room = Room(name=name,
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

    def testCreateCampOnSuccess(self):
        request = self.factory.post("/campon", {
                "camped_on_booking": 1,
                "end_time": "14:00"
            },
            format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))

        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 30, 0, 0), datetime):
            response = CampOnCreate.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_camp_on = CampOn.objects.last()

        self.assertEqual(created_camp_on.booker, self.user)
        self.assertEqual(created_camp_on.camped_on_booking, Booking.objects.get(id=1))
        self.assertEqual(created_camp_on.start_time, datetime.time(12, 30))

        self.assertEqual(created_camp_on.end_time, datetime.time(14, 00))

        # LogEntry test
        latest_campon_log = LogEntry.objects.last()
        self.assertEqual(latest_campon_log.action_flag, ADDITION)
        self.assertEqual(latest_campon_log.object_id, str(created_camp_on.id))
        self.assertEqual(latest_campon_log.user, self.user)
        self.assertEqual(latest_campon_log.change_message, json.dumps(LogCampOnSerializer(created_camp_on).data))

    @unittest.skip("emails are not sent in tests")
    def testCreateCampOnWithBooking(self):
        request = self.factory.post("/campon", {
            "camped_on_booking": 1,
            "end_time": "15:00"
        }, format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))

        # using 12:28 to test rounding
        with mock_datetime(datetime.datetime(2018, 1, 1, 12, 28, 0, 0), datetime):
            response = CampOnCreate.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 1)

        # Verify the content of the created CampOn
        created_camp_on = CampOn.objects.last()

        self.assertEqual(created_camp_on.booker, self.user)
        self.assertEqual(created_camp_on.camped_on_booking, Booking.objects.get(id=1))
        self.assertEqual(created_camp_on.start_time, datetime.time(12, 30))

        self.assertEqual(created_camp_on.end_time, datetime.time(14, 00))

        # Verify number of Booking
        self.assertEqual(len(Booking.objects.all()), 2)

        # Verify the content of the created Booking
        created_booking = Booking.objects.last()
        self.assertEqual(created_booking.booker, self.user)
        self.assertEqual(created_booking.room, Room.objects.get(name="H800-1"))
        self.assertEqual(created_booking.date, datetime.datetime.now().date())
        self.assertEqual(created_booking.start_time, datetime.time(14, 00))
        self.assertEqual(created_booking.end_time, datetime.time(15, 00))

        # LogEntry test
        all_campon_logs = LogEntry.objects.all()
        latest_campon_log = all_campon_logs.order_by('action_time')[0]
        self.assertEqual(latest_campon_log.action_flag, ADDITION)
        self.assertEqual(latest_campon_log.object_id, str(created_camp_on.id))
        self.assertEqual(latest_campon_log.user, self.user)
        self.assertEqual(latest_campon_log.change_message, json.dumps(LogCampOnSerializer(created_camp_on).data))

        # Generated Booking Log Entry
        all_booking_logs = LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(created_booking))
        latest_booking_log = all_booking_logs.order_by('action_time')[0]
        self.assertEqual(latest_booking_log.action_flag, ADDITION)
        self.assertEqual(latest_booking_log.object_id, str(created_booking.id))
        self.assertEqual(latest_booking_log.user, self.user)
        self.assertEqual(latest_booking_log.change_message, json.dumps(LogBookingSerializer(created_booking).data))

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
            response = CampOnCreate.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # Verify number of CampOn
        self.assertEqual(len(CampOn.objects.all()), 0)

    def testCreateCampOnNotAuthenticated(self):
        request = self.factory.post("/campon", {
            "camped_on_booking": 1,
            "end_time": "15:00"
        }, format="json")
        response = CampOnCreate.as_view()(request)

        # Verify none authorized request
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testCreateCampOnInvalidBooking(self):
        request = self.factory.post("/campon", {
            "camped_on_booking": 10,  # Booking id does not exist
            "end_time": "11:00"
        }, format="json")

        force_authenticate(request, user=User.objects.get(username="sol_ji"))
        response = CampOnCreate.as_view()(request)

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

        request = self.factory.get("/campons", {
            "id": 1
        }, format="json")

        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

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

        request = self.factory.get("/campons", {
            "booking_id": 1
        }, format="json")

        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

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

        request = self.factory.get("/campons", {
            "booking_id": 1,
            "start_time": "12:20",
            "end_time": "13:00"
        }, format="json")

        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

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

        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

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

        request = self.factory.get("/campons", {
        }, format="json")

        response = CampOnList.as_view()(request)

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

        request = self.factory.get("/campons", {
            "id": 10,
        },
                                   format="json")
        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def testGetEmptyCampOn(self):
        request = self.factory.get("/campons", {
        }, format="json")

        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def testGetCampOnWithInvalidCampOnId(self):
        request = self.factory.get("/campons", {
            "id": str
        }, format="json")
        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def testGetCampOnWithInvalidBookingId(self):
        request = self.factory.get("/campons", {
            "booking_id": str
        }, format="json")
        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def testGetCampOnWithInvalidStartTime(self):
        request = self.factory.get("/campons", {
            "start_time": "str",
            "end_time": self.end_time,
        }, format="json")
        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def testGetCampOnWithInvalidEndTime(self):
        request = self.factory.get("/campons", {
            "start_time": self.start_time,
            "end_time": str,
        }, format="json")
        response = CampOnList.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
