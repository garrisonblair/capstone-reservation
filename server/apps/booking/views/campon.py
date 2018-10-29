from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.models.Student import Student
from apps.booking.models.CampOn import CampOn
from apps.booking.models.Booking import Booking
from apps.booking.serializers.campon_serializer import CampOnSerializer
from apps.booking.serializers.booking_serializer import BookingSerializer
import datetime


class CampOnView(APIView):

    def post(self, request):

        # Must be logged in as student
        if not request.user or not request.user.student:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        campon_data = dict(request.data)
        campon_data["student"] = request.user.student.student_id
        campon_data["start_time"] = datetime.datetime.now().time()
        serializer = CampOnSerializer(data=campon_data)

        print(campon_data["start_time"])

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:

            current_booking = Booking.objects.get(id=campon_data["booking"])
            request_end_time = datetime.datetime.strptime(campon_data["end_time"], "%H:%M").time()

            if request_end_time > current_booking.end_time:

                found_bookings = Booking.objects.filter(
                                    start_time__range=(current_booking.end_time, request_end_time))

                if found_bookings:
                    return Response("End time overlaps with future booking", status=status.HTTP_409_CONFLICT)
                # No Booking found, create new Booking and create CampOn

                campon_data["end_time"] = current_booking.end_time
                new_campon_serializer = CampOnSerializer(data=campon_data)
                campon = new_campon_serializer.save()

                new_booking = Booking(student=campon.student,
                                      student_group=campon.camped_on_booking.student_group,
                                      room=campon.camped_on_booking.room,
                                      date=campon.camped_on_booking.date,
                                      start_time=campon.end_time,
                                      end_time=request_end_time)

                response_data = {"CampOn": CampOnSerializer(campon).data,
                                 "Booking": BookingSerializer(new_booking).data}
                return Response(response_data, status=status.HTTP_201_CREATED)

            campon = serializer.save()
            return Response({"CampOn": CampOnSerializer(campon).data}, status=status.HTTP_201_CREATED)

        except (ValueError, ValidationError) as error:
            return Response(error.messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        request_id = request.GET.get('id')
        request_booking = request.GET.get('booking')
        request_start_time = request.GET.get('start_time')
        request_end_time = request.GET.get('end_time')

        try:
            if request_id is not None:
                campons = CampOn.objects.filter(id=request_id)
            elif not(not request_booking or not request_start_time or not request_end_time):
                campons = CampOn.objects.filter(booking=request_booking,
                                                start_time=request_start_time,
                                                end_time=request_end_time)
            elif not(not request_start_time or not request_end_time):
                campons = CampOn.objects.filter(start_time=request_start_time, end_time=request_end_time)
            elif request_booking is not None:
                campons = CampOn.objects.filter(booking=request_booking)
            else:
                campons = CampOn.objects.all()
        except (ValueError, ValidationError) as error:
            return Response("Input value is invalid.", status=status.HTTP_400_BAD_REQUEST)

        campon_list = list()
        for campon in campons:
            serializer = CampOnSerializer(campon)
            campon_list.append(serializer.data)
        return Response(campon_list, status=status.HTTP_200_OK)

    def createNewCampOn(self, campon_data, booking, start_time, request_end_time, booking_end_time):
        campon_data["booking"] = booking
        campon_data["start_time"] = start_time
        if request_end_time > booking_end_time:
            campon_data["end_time"] = booking_end_time
        else:
            campon_data["end_time"] = request_end_time
        new_campon_serializer = CampOnSerializer(data=campon_data)

        if not new_campon_serializer.is_valid():
            return "New CampOn creation fails on Booking {}".format(booking)
        new_campon = new_campon_serializer.save()
        return CampOnSerializer(new_campon).data

    def createNewBooking(self, student_id, room, date, start_time, end_time):
        new_booking_serializer = BookingSerializer(data={'student': student_id,
                                                         'room': room,
                                                         'date': date,
                                                         'start_time': start_time,
                                                         'end_time': end_time})
        if not new_booking_serializer.is_valid():
            return "New Booking creation fails with start time {} and end time {}".format(start_time, end_time)
        new_booking = new_booking_serializer.save()
        return BookingSerializer(new_booking).data
