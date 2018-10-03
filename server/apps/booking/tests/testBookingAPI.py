from django.test.testcases import TestCase
from rest_framework.test import APIRequestFactory

from apps.accounts.models.Student import Student
from apps.rooms.models.Room import Room
from ..models.Booking import Booking

from ..views.booking import BookingView


class BookingAPITest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        student = Student(student_id="f_daigl")
        student.save()

        room = Room(room_id="H833-17", capacity=4, number_of_computers=1)
        room.save()



    def testPOST(self):


        request = self.factory.post("/booking",
                                    {
                                        "student": "27203780",
                                        "room": 1,
                                        "date": "2019-08-10",
                                        "start_time": "14:00:00",
                                        "end_time": "15:00:00"
                                    })

        response = BookingView.as_view(request)

        bookings = Booking.objects.all()

        print(len(bookings))
